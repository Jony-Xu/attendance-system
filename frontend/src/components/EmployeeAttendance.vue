<template>
  <div class="employee-attendance">
    <h2 class="ui header">
      <i class="user check icon"></i>
      <div class="content">
        员工考勤
        <div class="sub header">签到签退管理</div>
      </div>
    </h2>

    <!-- 员工选择 -->
    <div class="ui segment">
      <h3 class="ui dividing header">选择员工</h3>
      <div class="ui form">
        <div class="field">
          <label>员工</label>
          <select v-model="selectedEmployeeId" class="ui dropdown" @change="onEmployeeChange">
            <option value="">请选择员工</option>
            <option v-for="emp in employees" :key="emp.id" :value="emp.id">
              {{ emp.name }} ({{ emp.employee_id }})
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- 当前状态 -->
    <div v-if="selectedEmployeeId" class="ui segment">
      <h3 class="ui dividing header">当前状态</h3>
      <div v-if="attendanceStatus" class="ui statistics">
        <div class="statistic">
          <div class="value">
            <i :class="statusIcon"></i>
          </div>
          <div class="label">{{ statusText }}</div>
        </div>
        <div v-if="attendanceStatus.last_timestamp" class="statistic">
          <div class="value">
            {{ formatTime(attendanceStatus.last_timestamp) }}
          </div>
          <div class="label">最后操作时间</div>
        </div>
      </div>
    </div>

    <!-- 考勤操作 -->
    <div v-if="selectedEmployeeId" class="ui segment">
      <h3 class="ui dividing header">考勤操作</h3>
      <div class="ui form">
        <div class="field">
          <label>备注</label>
          <textarea v-model="notes" rows="2" placeholder="可选：添加备注信息"></textarea>
        </div>
        <div class="ui two buttons">
          <button 
            class="ui green button" 
            @click="checkIn"
            :disabled="!canCheckIn"
            :class="{ loading: loading }"
          >
            <i class="sign in icon"></i>
            签到
          </button>
          <button 
            class="ui orange button" 
            @click="checkOut"
            :disabled="!canCheckOut"
            :class="{ loading: loading }"
          >
            <i class="sign out icon"></i>
            签退
          </button>
        </div>
      </div>
    </div>

    <!-- 今日记录 -->
    <div v-if="selectedEmployeeId && todayRecords.length > 0" class="ui segment">
      <h3 class="ui dividing header">今日记录</h3>
      <table class="ui celled table">
        <thead>
          <tr>
            <th>类型</th>
            <th>时间</th>
            <th>备注</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in todayRecords" :key="record.id">
            <td>
              <span :class="['ui label', record.attendance_type === 'check_in' ? 'green' : 'orange']">
                {{ record.attendance_type === 'check_in' ? '签到' : '签退' }}
              </span>
            </td>
            <td>{{ formatDateTime(record.timestamp) }}</td>
            <td>{{ record.notes || '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 消息提示 -->
    <div v-if="message" :class="['ui message', messageType]">
      <i class="close icon" @click="message = ''"></i>
      <div class="header">{{ message }}</div>
    </div>
  </div>
</template>

<script>
import { employeeAPI, attendanceAPI } from '../api'

export default {
  name: 'EmployeeAttendance',
  data() {
    return {
      employees: [],
      selectedEmployeeId: '',
      attendanceStatus: null,
      todayRecords: [],
      notes: '',
      loading: false,
      message: '',
      messageType: 'info'
    }
  },
  computed: {
    canCheckIn() {
      return this.attendanceStatus && 
             (this.attendanceStatus.status === 'not_checked_in' || 
              this.attendanceStatus.status === 'checked_out')
    },
    canCheckOut() {
      return this.attendanceStatus && 
             this.attendanceStatus.status === 'checked_in'
    },
    statusIcon() {
      if (!this.attendanceStatus) return 'question circle icon'
      switch (this.attendanceStatus.status) {
        case 'not_checked_in': return 'circle outline icon'
        case 'checked_in': return 'check circle icon green'
        case 'checked_out': return 'check circle icon orange'
        default: return 'question circle icon'
      }
    },
    statusText() {
      if (!this.attendanceStatus) return '未知'
      switch (this.attendanceStatus.status) {
        case 'not_checked_in': return '未签到'
        case 'checked_in': return '已签到'
        case 'checked_out': return '已签退'
        default: return '未知'
      }
    }
  },
  mounted() {
    this.loadEmployees()
  },
  methods: {
    async loadEmployees() {
      try {
        const response = await employeeAPI.getAll()
        this.employees = response.data.filter(emp => emp.is_active)
      } catch (error) {
        this.showMessage('加载员工列表失败', 'error')
      }
    },
    async onEmployeeChange() {
      if (this.selectedEmployeeId) {
        await this.loadAttendanceStatus()
        await this.loadTodayRecords()
      }
    },
    async loadAttendanceStatus() {
      try {
        const response = await attendanceAPI.getStatus(this.selectedEmployeeId)
        this.attendanceStatus = response.data
      } catch (error) {
        this.showMessage('加载考勤状态失败', 'error')
      }
    },
    async loadTodayRecords() {
      try {
        const response = await attendanceAPI.getRecords({
          employee_id: this.selectedEmployeeId,
          limit: 10
        })
        const today = new Date().toDateString()
        this.todayRecords = response.data.filter(record => 
          new Date(record.timestamp).toDateString() === today
        )
      } catch (error) {
        console.error('加载今日记录失败', error)
      }
    },
    async checkIn() {
      this.loading = true
      try {
        await attendanceAPI.checkIn(this.selectedEmployeeId, {
          notes: this.notes
        })
        this.showMessage('签到成功！', 'success')
        this.notes = ''
        await this.loadAttendanceStatus()
        await this.loadTodayRecords()
      } catch (error) {
        this.showMessage(error.response?.data?.detail || '签到失败', 'error')
      } finally {
        this.loading = false
      }
    },
    async checkOut() {
      this.loading = true
      try {
        await attendanceAPI.checkOut(this.selectedEmployeeId, {
          notes: this.notes
        })
        this.showMessage('签退成功！', 'success')
        this.notes = ''
        await this.loadAttendanceStatus()
        await this.loadTodayRecords()
      } catch (error) {
        this.showMessage(error.response?.data?.detail || '签退失败', 'error')
      } finally {
        this.loading = false
      }
    },
    showMessage(msg, type = 'info') {
      this.message = msg
      this.messageType = type
      setTimeout(() => {
        this.message = ''
      }, 5000)
    },
    formatTime(timestamp) {
      const date = new Date(timestamp)
      return date.toLocaleTimeString('zh-CN')
    },
    formatDateTime(timestamp) {
      const date = new Date(timestamp)
      return date.toLocaleString('zh-CN')
    }
  }
}
</script>

<style scoped>
.employee-attendance {
  max-width: 800px;
  margin: 0 auto;
}
</style>
