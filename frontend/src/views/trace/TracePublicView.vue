<template>
  <div class="trace-page">
    <div class="trace-header">
      <h2>🍎 农产品溯源查询</h2>
      <p>基于国密区块链 · 数据不可篡改</p>
    </div>

    <div class="search-bar">
      <el-input
        v-model="inputCode"
        placeholder="请输入溯源批次号"
        size="large"
        clearable
        style="max-width: 500px"
        @keyup.enter="doQuery"
      >
        <template #append>
          <el-button type="primary" :loading="loading" @click="doQuery">查询</el-button>
        </template>
      </el-input>
    </div>

    <div v-if="traceData" class="trace-result">
      <!-- 产品基本信息 -->
      <el-card class="product-card">
        <template #header>
          <span>产品基本信息</span>
          <el-tag :type="statusType" style="float: right">{{ traceData.status_label }}</el-tag>
        </template>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="批次号">{{ traceData.batch_no }}</el-descriptions-item>
          <el-descriptions-item label="产品名称">{{ traceData.product_name }}</el-descriptions-item>
          <el-descriptions-item label="产品类型">{{ traceData.product_type }}</el-descriptions-item>
          <el-descriptions-item label="数量">{{ traceData.quantity }} {{ traceData.unit }}</el-descriptions-item>
          <el-descriptions-item label="产地信息" :span="2">{{ traceData.origin_info }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 溯源时间轴 -->
      <el-card class="timeline-card">
        <template #header>溯源时间轴</template>
        <el-timeline>
          <el-timeline-item
            v-for="node in traceData.timeline"
            :key="node.id"
            :timestamp="node.operation_time"
            placement="top"
            :type="nodeTypeColor(node.node_type)"
          >
            <el-card class="node-card">
              <div class="node-header">
                <el-tag :type="nodeTypeColor(node.node_type)">{{ node.node_label }}</el-tag>
                <span class="location">📍 {{ node.location }}</span>
              </div>
              <div class="node-env" v-if="node.env_data">
                <span v-for="(val, key) in node.env_data" :key="key" class="env-item">
                  {{ key }}: {{ val }}
                </span>
              </div>
              <div class="node-chain">
                <el-tooltip :content="node.tx_hash" placement="top">
                  <span class="chain-hash">🔗 区块哈希: {{ node.tx_hash?.slice(0, 20) }}...</span>
                </el-tooltip>
                <span class="block-height">区块高度: {{ node.block_height }}</span>
              </div>
              <div v-if="node.ipfs_files?.length" class="ipfs-files">
                <a
                  v-for="f in node.ipfs_files"
                  :key="f.cid"
                  :href="f.url"
                  target="_blank"
                  class="ipfs-link"
                >
                  📎 {{ f.file_name }}
                </a>
              </div>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </el-card>
    </div>

    <el-empty v-else-if="queried && !loading" description="未找到溯源信息，请检查批次号" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { queryByTraceCode } from '../../api/trace'

const route = useRoute()
const inputCode = ref((route.params.code as string) || '')
const loading = ref(false)
const queried = ref(false)
const traceData = ref<any>(null)

const nodeTypeColor = (type: string) => {
  const map: Record<string, any> = {
    planting: 'success',
    harvesting: 'warning',
    inspecting: 'primary',
    packing: '',
    transporting: 'info',
    retailing: 'danger',
  }
  return map[type] || ''
}

const statusType = computed(() => {
  const map: Record<number, any> = { 0: 'info', 1: 'warning', 2: 'primary', 3: 'warning', 4: 'success' }
  return map[traceData.value?.status] || 'info'
})

const doQuery = async () => {
  if (!inputCode.value.trim()) {
    ElMessage.warning('请输入溯源批次号')
    return
  }
  loading.value = true
  queried.value = true
  try {
    traceData.value = await queryByTraceCode(inputCode.value.trim())
  } catch {
    traceData.value = null
  } finally {
    loading.value = false
  }
}

// 如果路由携带了溯源码，自动查询
if (inputCode.value) {
  doQuery()
}
</script>

<style scoped>
.trace-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px 16px;
}
.trace-header {
  text-align: center;
  margin-bottom: 24px;
}
.trace-header h2 { font-size: 28px; color: #1a5276; }
.trace-header p { color: #888; margin-top: 4px; }
.search-bar {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}
.product-card, .timeline-card { margin-bottom: 16px; }
.node-card { background: #fafafa; }
.node-header { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
.location { color: #666; font-size: 13px; }
.node-env { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 8px; }
.env-item {
  background: #e8f5e9;
  color: #2e7d32;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}
.node-chain { display: flex; gap: 16px; font-size: 12px; color: #888; margin-bottom: 6px; }
.chain-hash { cursor: pointer; }
.chain-hash:hover { color: #1a5276; }
.ipfs-files { display: flex; flex-wrap: wrap; gap: 8px; }
.ipfs-link { font-size: 12px; color: #27ae60; text-decoration: none; }
.ipfs-link:hover { text-decoration: underline; }
</style>
