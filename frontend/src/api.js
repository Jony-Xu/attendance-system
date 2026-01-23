import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// 员工相关
export const employeeAPI = {
  getAll: () => api.get('/employees/'),
  getById: (id) => api.get(`/employees/${id}`),
  create: (data) => api.post('/employees/', data),
  update: (id, data) => api.put(`/employees/${id}`, data)
}

// 考勤相关
export const attendanceAPI = {
  checkIn: (employeeId, data = {}) => api.post('/attendance/check-in', null, {
    params: { employee_id: employeeId, ...data }
  }),
  checkOut: (employeeId, data = {}) => api.post('/attendance/check-out', null, {
    params: { employee_id: employeeId, ...data }
  }),
  getRecords: (params = {}) => api.get('/attendance/records', { params }),
  getMonthly: (year, month, employeeId = null) => {
    const params = employeeId ? { employee_id: employeeId } : {}
    return api.get(`/attendance/monthly/${year}/${month}`, { params })
  },
  getStatus: (employeeId) => api.get(`/attendance/status/${employeeId}`)
}

// 工作时间相关
export const scheduleAPI = {
  getAll: (activeOnly = true) => api.get('/schedules/', {
    params: { active_only: activeOnly }
  }),
  getById: (id) => api.get(`/schedules/${id}`),
  getActive: () => api.get('/schedules/active'),
  create: (data) => api.post('/schedules/', data),
  update: (id, data) => api.put(`/schedules/${id}`, data),
  activate: (id) => api.post(`/schedules/${id}/activate`),
  delete: (id) => api.delete(`/schedules/${id}`)
}

export default api
