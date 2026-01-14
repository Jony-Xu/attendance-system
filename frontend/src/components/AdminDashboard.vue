<template>
  <div class="admin-dashboard">
    <h2 class="ui header">
      <i class="settings icon"></i>
      <div class="content">
        管理后台
        <div class="sub header">工作时间设置与考勤记录查看</div>
      </div>
    </h2>

    <div class="ui two column stackable grid">
      <!-- 左侧：工作时间管理 -->
      <div class="column">
        <div class="ui segment">
          <h3 class="ui dividing header">
            <i class="clock outline icon"></i>
            工作时间设置
          </h3>

          <!-- 当前激活的工作时间 -->
          <div v-if="activeSchedule" class="ui info message">
            <div class="header">当前工作时间</div>
            <p>
              <strong>{{ activeSchedule.name }}</strong><br>
              上班时间: {{ activeSchedule.check_in_time }}<br>
              下班时间: {{ activeSchedule.check_out_time }}
            </p>
          </div>

          <!-- 添加新工作时间 -->
          <div class="ui form">
            <h4>添加工作时间</h4>
            <div class="field">
              <label>名称</label>
              <input v-model="newSchedule.name" placeholder="例如：标准工作时间">
            </div>
            <div class="two fields">
              <div class="field">
                <label>上班时间</label>
                <input v-model="newSchedule.check_in_time" type="time">
              </div>
              <div class="field">
                <label>下班时间</label>
                <input v-model="newSchedule.check_out_time" type="time">
              </div>
            </div>
            <button class="ui primary button" @click="createSchedule" :class="{ loading: loadingSchedule }">
              <i class="plus icon"></i>
              添加
            </button>
          </div>

          <!-- 工作时间列表 -->
          <div class="ui divider"></div>
          <h4>所有工作时间</h4>
          <div class="ui relaxed list">
            <div v-for="schedule in schedules" :key="schedule.id" class="item">
              <div class="content">
                <div class="header">
                  {{ schedule.name }}
                  <span v-if="schedule.is_active" class="ui green label">当前激活</span>
                </div>
                <div class="description">
                  {{ schedule.check_in_time }} - {{ schedule.check_out_time }}
                </div>
                <div class="ui mini buttons" style="margin-top: 0.5em;">
                  <button 
                    v-if="!schedule.is_active"
                    class="ui button"
                    @click="activateSchedule(schedule.id)"
                  >
                    激活
                  </button>
                  <button 
                    class="ui button"
                    @click="editSchedule(schedule)"
                  >
                    编辑
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：考勤记录查看 -->
      <div class="column">
        <div class="ui segment">
          <h3 class="ui dividing header">
            <i class="calendar alternate outline icon"></i>
            考勤记录查询
          </h3>

          <!-- 查询条件 -->
          <div class="ui form">
            <div class="field">
              <label>选择月份</label>
              <div class="two fields">
                <div class="field">
                  <input v-model="queryYear" type="number" placeholder="年份" min="2020" max="2030">
                </div>
                <div class="field">
                  <input v-model="queryMonth" type="number" placeholder="月份" min="1" max="12">
                </div>
              </div>
            </div>
            <div class="field">
              <label>员工（可选）</label>
              <select v-model="queryEmployeeId" class="ui dropdown">
                <option value="">所有员工</option>
                <option v-for="emp in employees" :key="emp.id" :value="emp.id">
                  {{ emp.name }} ({{ emp.employee_id }})
                </option>
              </select>
            </div>
            <button class="ui primary button" @click="loadMonthlyRecords" :class="{ loading: loadingRecords }">
              <i class="search icon"></i>
              查询
            </button>
          </div>

          <!-- 统计信息 -->
          <div v-if="monthlyStats" class="ui statistics" style="margin-top: 1em;">
            <div class="statistic">
              <div class="value">{{ monthlyStats.total_records }}</div>
              <div class="label">总记录</div>
            </div>
            <div class="statistic">
              <div class="value">{{ monthlyStats.check_in_count }}</div>
              <div class="label">签到</div>
            </div>
            <div class="statistic">
              <div class="value">{{ monthlyStats.check_out_count }}</div>
              <div class="label">签退</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 考勤记录详情表格 -->
    <div v-if="monthlyRecords.length > 0" class="ui segment">
      <h3 class="ui dividing header">考勤记录详情</h3>
      <table class="ui celled table">
        <thead>
          <tr>
            <th>员工</th>
            <th>员工编号</th>
            <th>类型</th>
            <th>时间</th>
            <th>备注</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in monthlyRecords" :key="record.id">
            <td>{{ record.employee.name }}</td>
            <td>{{ record.employee.employee_id }}</td>
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

    <!-- 编辑工作时间模态框 -->
    <div v-if="editingSchedule" class="ui modal active">
      <div class="header">编辑工作时间</div>
      <div class="content">
        <div class="ui form">
          <div class="field">
            <label>名称</label>
            <input v-model="editingSchedule.name">
          </div>
          <div class="two fields">
            <div class="field">
              <label>上班时间</label>
              <input v-model="editingSchedule.check_in_time" type="time">
            </div>
            <div class="field">
              <label>下班时间</label>
              <input v-model="editingSchedule.check_out_time" type="time">
            </div>
          </div>
        </div>
      </div>
      <div class="actions">
        <button class="ui cancel button" @click="cancelEdit">取消</button>
        <button class="ui primary button" @click="updateSchedule">保存</button>
      </div>
    </div>

    <!-- 消息提示 -->
    <div v-if="message" :class="['ui message', messageType]" style="margin-top: 1em;">
      <i class="close icon" @click="message = ''"></i>
      <div class="header">{{ message }}</div>
    </div>
  </div>
</template>

<script>
import { scheduleAPI, attendanceAPI, employeeAPI } from '../api'

export default {
  name: 'AdminDashboard',
  data() {
    return {
      activeSchedule: null,
      schedules: [],
      employees: [],
      newSchedule: {
        name: '',
        check_in_time: '09:00',
        check_out_time: '18:00'
      },
      editingSchedule: null,
      queryYear: new Date().getFullYear(),
      queryMonth: new Date().getMonth() + 1,
      queryEmployeeId: '',
      monthlyStats: null,
      monthlyRecords: [],
      loadingSchedule: false,
      loadingRecords: false,
      message: '',
      messageType: 'info'
    }
  },
  mounted() {
    this.loadSchedules()
    this.loadEmployees()
  },
  methods: {
    async loadSchedules() {
      try {
        const [activeRes, allRes] = await Promise.all([
          scheduleAPI.getActive().catch(() => ({ data: null })),
          scheduleAPI.getAll(false)
        ])
        this.activeSchedule = activeRes.data
        this.schedules = allRes.data
      } catch (error) {
        this.showMessage('加载工作时间失败', 'error')
      }
    },
    async loadEmployees() {
      try {
        const response = await employeeAPI.getAll()
        this.employees = response.data
      } catch (error) {
        this.showMessage('加载员工列表失败', 'error')
      }
    },
    async createSchedule() {
      if (!this.newSchedule.name || !this.newSchedule.check_in_time || !this.newSchedule.check_out_time) {
        this.showMessage('请填写完整信息', 'warning')
        return
      }

      this.loadingSchedule = true
      try {
        await scheduleAPI.create({
          name: this.newSchedule.name,
          check_in_time: this.newSchedule.check_in_time + ':00',
          check_out_time: this.newSchedule.check_out_time + ':00'
        })
        this.showMessage('工作时间添加成功', 'success')
        this.newSchedule = {
          name: '',
          check_in_time: '09:00',
          check_out_time: '18:00'
        }
        await this.loadSchedules()
      } catch (error) {
        this.showMessage(error.response?.data?.detail || '添加失败', 'error')
      } finally {
        this.loadingSchedule = false
      }
    },
    async activateSchedule(scheduleId) {
      try {
        await scheduleAPI.activate(scheduleId)
        this.showMessage('工作时间已激活', 'success')
        await this.loadSchedules()
      } catch (error) {
        this.showMessage('激活失败', 'error')
      }
    },
    editSchedule(schedule) {
      this.editingSchedule = {
        ...schedule,
        check_in_time: schedule.check_in_time.slice(0, 5),
        check_out_time: schedule.check_out_time.slice(0, 5)
      }
    },
    cancelEdit() {
      this.editingSchedule = null
    },
    async updateSchedule() {
      try {
        await scheduleAPI.update(this.editingSchedule.id, {
          name: this.editingSchedule.name,
          check_in_time: this.editingSchedule.check_in_time + ':00',
          check_out_time: this.editingSchedule.check_out_time + ':00'
        })
        this.showMessage('更新成功', 'success')
        this.editingSchedule = null
        await this.loadSchedules()
      } catch (error) {
        this.showMessage('更新失败', 'error')
      }
    },
    async loadMonthlyRecords() {
      if (!this.queryYear || !this.queryMonth) {
        this.showMessage('请选择年月', 'warning')
        return
      }

      this.loadingRecords = true
      try {
        const response = await attendanceAPI.getMonthly(
          this.queryYear,
          this.queryMonth,
          this.queryEmployeeId || null
        )
        this.monthlyStats = {
          total_records: response.data.total_records,
          check_in_count: response.data.check_in_count,
          check_out_count: response.data.check_out_count
        }
        this.monthlyRecords = response.data.records
      } catch (error) {
        this.showMessage('查询失败', 'error')
      } finally {
        this.loadingRecords = false
      }
    },
    showMessage(msg, type = 'info') {
      this.message = msg
      this.messageType = type
      setTimeout(() => {
        this.message = ''
      }, 5000)
    },
    formatDateTime(timestamp) {
      const date = new Date(timestamp)
      return date.toLocaleString('zh-CN')
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

.ui.modal.active {
  display: block !important;
  position: fixed;
  z-index: 1000;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  background: white;
  box-shadow: 0 0 20px rgba(0,0,0,0.3);
  padding: 1em;
  border-radius: 0.28571429rem;
}
</style>
