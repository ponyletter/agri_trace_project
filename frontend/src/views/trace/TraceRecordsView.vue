<template>
  <el-container class="layout">
    <el-aside width="220px" class="sidebar">
      <div class="sidebar-logo">🌾 农产品溯源系统</div>
      <el-menu router background-color="#1a3a5c" text-color="#c0d8f0" active-text-color="#ffffff">
        <el-menu-item index="/dashboard"><el-icon><DataBoard /></el-icon><span>系统概览</span></el-menu-item>
        <el-menu-item index="/batches"><el-icon><Box /></el-icon><span>批次管理</span></el-menu-item>
        <el-menu-item index="/trace-records"><el-icon><List /></el-icon><span>溯源记录</span></el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <span class="header-title">溯源记录管理</span>
        <el-button type="primary" @click="showAdd = true">添加溯源记录</el-button>
      </el-header>
      <el-main>
        <el-table :data="records" stripe border>
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="batch_id" label="批次ID" width="80" />
          <el-table-column prop="node_type" label="节点类型" width="100">
            <template #default="{ row }">
              <el-tag>{{ nodeLabel(row.node_type) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="location" label="操作地点" min-width="160" />
          <el-table-column prop="operation_time" label="操作时间" width="170" />
          <el-table-column prop="tx_hash" label="交易哈希" min-width="180">
            <template #default="{ row }">
              <el-tooltip :content="row.tx_hash">
                <span style="cursor: pointer; color: #1a5276">{{ row.tx_hash?.slice(0, 18) }}...</span>
              </el-tooltip>
            </template>
          </el-table-column>
          <el-table-column prop="block_height" label="区块高度" width="100" />
        </el-table>
      </el-main>
    </el-container>
  </el-container>

  <!-- 添加溯源记录对话框 -->
  <el-dialog v-model="showAdd" title="添加溯源节点记录" width="560px">
    <el-form :model="addForm" label-width="110px">
      <el-form-item label="批次ID"><el-input-number v-model="addForm.batch_id" :min="1" /></el-form-item>
      <el-form-item label="节点类型">
        <el-select v-model="addForm.node_type">
          <el-option v-for="n in nodeTypes" :key="n.value" :label="n.label" :value="n.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="操作时间">
        <el-date-picker v-model="addForm.operation_time" type="datetime" format="YYYY-MM-DD HH:mm:ss" value-format="YYYY-MM-DD HH:mm:ss" />
      </el-form-item>
      <el-form-item label="操作地点"><el-input v-model="addForm.location" /></el-form-item>
      <el-form-item label="扩展数据(JSON)">
        <el-input v-model="envDataStr" type="textarea" :rows="3" placeholder='{"temperature": "25°C"}' />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="showAdd = false">取消</el-button>
      <el-button type="primary" :loading="adding" @click="doAdd">提交上链</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { listTraceRecords, addTraceRecord } from '../../api/trace'

const records = ref<any[]>([])
const showAdd = ref(false)
const adding = ref(false)
const envDataStr = ref('')
const addForm = ref({ batch_id: 1, node_type: 'planting', operation_time: '', location: '' })

const nodeTypes = [
  { value: 'planting', label: '种植' }, { value: 'harvesting', label: '采收' },
  { value: 'inspecting', label: '质检' }, { value: 'packing', label: '装箱' },
  { value: 'transporting', label: '运输' }, { value: 'retailing', label: '上架' },
]
const nodeLabel = (t: string) => nodeTypes.find(n => n.value === t)?.label || t

const loadRecords = async () => {
  try { records.value = ((await listTraceRecords()) as unknown) as any[] } catch {}
}

const doAdd = async () => {
  adding.value = true
  try {
    let envData = {}
    if (envDataStr.value.trim()) {
      try { envData = JSON.parse(envDataStr.value) } catch { ElMessage.error('扩展数据JSON格式错误'); return }
    }
    await addTraceRecord({ ...addForm.value, env_data: envData })
    ElMessage.success('溯源记录添加成功，已上链')
    showAdd.value = false
    loadRecords()
  } finally { adding.value = false }
}

onMounted(loadRecords)
</script>

<style scoped>
.layout { min-height: 100vh; }
.sidebar { background: #1a3a5c; }
.sidebar-logo { height: 60px; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 15px; font-weight: 600; border-bottom: 1px solid #2d5a8e; }
.header { background: #fff; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #e8e8e8; padding: 0 20px; }
.header-title { font-size: 16px; font-weight: 600; color: #333; }
</style>
