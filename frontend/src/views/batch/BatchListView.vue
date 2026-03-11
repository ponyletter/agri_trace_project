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
        <span class="header-title">批次管理</span>
        <el-button type="primary" @click="showCreate = true">新建批次</el-button>
      </el-header>
      <el-main>
        <el-table :data="batches" stripe border>
          <el-table-column prop="batch_no" label="批次号" min-width="200" />
          <el-table-column prop="product_name" label="产品名称" width="140" />
          <el-table-column prop="quantity" label="数量" width="100">
            <template #default="{ row }">{{ row.quantity }} {{ row.unit }}</template>
          </el-table-column>
          <el-table-column prop="origin_info" label="产地" min-width="160" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="statusType(row.status)">{{ statusLabel(row.status) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120">
            <template #default="{ row }">
              <el-button size="small" @click="viewTrace(row.batch_no)">溯源</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>
  </el-container>

  <!-- 新建批次对话框 -->
  <el-dialog v-model="showCreate" title="新建农产品批次" width="500px">
    <el-form :model="createForm" label-width="100px">
      <el-form-item label="产品名称"><el-input v-model="createForm.product_name" /></el-form-item>
      <el-form-item label="产品类型"><el-input v-model="createForm.product_type" /></el-form-item>
      <el-form-item label="数量">
        <el-input-number v-model="createForm.quantity" :min="0" style="width: 150px" />
        <el-input v-model="createForm.unit" placeholder="单位" style="width: 80px; margin-left: 8px" />
      </el-form-item>
      <el-form-item label="产地信息"><el-input v-model="createForm.origin_info" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="showCreate = false">取消</el-button>
      <el-button type="primary" :loading="creating" @click="doCreate">确认创建</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { listBatches, createBatch } from '../../api/trace'

const router = useRouter()
const batches = ref<any[]>([])
const showCreate = ref(false)
const creating = ref(false)
const createForm = ref({ product_name: '', product_type: '果蔬类', quantity: 0, unit: 'kg', origin_info: '' })

const statusLabel = (s: number) => ['种植中', '已采收', '已质检', '运输中', '已上架'][s] || '未知'
const statusType = (s: number) => (['info', 'warning', 'primary', 'warning', 'success'] as any[])[s] || ''

const loadBatches = async () => {
  try { batches.value = ((await listBatches()) as unknown) as any[] } catch {}
}

const doCreate = async () => {
  creating.value = true
  try {
    await createBatch(createForm.value)
    ElMessage.success('批次创建成功')
    showCreate.value = false
    loadBatches()
  } finally { creating.value = false }
}

const viewTrace = (batchNo: string) => router.push(`/trace/${batchNo}`)

onMounted(loadBatches)
</script>

<style scoped>
.layout { min-height: 100vh; }
.sidebar { background: #1a3a5c; }
.sidebar-logo { height: 60px; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 15px; font-weight: 600; border-bottom: 1px solid #2d5a8e; }
.header { background: #fff; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #e8e8e8; padding: 0 20px; }
.header-title { font-size: 16px; font-weight: 600; color: #333; }
</style>
