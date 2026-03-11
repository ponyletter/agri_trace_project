import request from './request'

// ==================== 认证接口 ====================
export const login = (data: { username: string; password: string }) =>
  request.post('/api/v1/auth/login', data)

export const getProfile = () => request.get('/api/v1/auth/profile')

export const register = (data: {
  username: string
  password: string
  real_name: string
  role: string
  phone?: string
}) => request.post('/api/v1/auth/register', data)

// ==================== 批次接口 ====================
export const createBatch = (data: {
  product_name: string
  product_type: string
  quantity: number
  unit: string
  origin_info: string
}) => request.post('/api/v1/batches', data)

export const listBatches = () => request.get('/api/v1/batches')

// ==================== 溯源接口 ====================
export const addTraceRecord = (data: {
  batch_id: number
  node_type: string
  operation_time: string
  location: string
  env_data?: Record<string, unknown>
}) => request.post('/api/v1/trace/records', data)

export const queryByTraceCode = (traceCode: string) =>
  request.get(`/api/v1/trace/${traceCode}`)

export const listTraceRecords = (batchId?: number) =>
  request.get('/api/v1/trace/records', { params: { batch_id: batchId } })

export const getBlockInfo = (height: number) =>
  request.get('/api/v1/block/info', { params: { height } })
