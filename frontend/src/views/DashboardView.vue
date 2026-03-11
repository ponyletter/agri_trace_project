<template>
  <el-container class="layout">
    <!-- 侧边栏 -->
    <el-aside width="220px" class="sidebar">
      <div class="sidebar-logo">
        <span>🌾 农产品溯源系统</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        router
        background-color="#1a3a5c"
        text-color="#c0d8f0"
        active-text-color="#ffffff"
      >
        <el-menu-item index="/dashboard">
          <el-icon><DataBoard /></el-icon>
          <span>系统概览</span>
        </el-menu-item>
        <el-menu-item index="/batches">
          <el-icon><Box /></el-icon>
          <span>批次管理</span>
        </el-menu-item>
        <el-menu-item index="/trace-records">
          <el-icon><List /></el-icon>
          <span>溯源记录</span>
        </el-menu-item>
        <el-menu-item v-if="isAdmin" index="/admin/users">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区 -->
    <el-container>
      <el-header class="header">
        <span class="header-title">系统概览</span>
        <div class="header-right">
          <el-tag type="success" size="small">区块链: 已连接</el-tag>
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              {{ userInfo?.real_name || userInfo?.username }}
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main>
        <el-row :gutter="16" class="stat-cards">
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-num">{{ stats.batches }}</div>
              <div class="stat-label">农产品批次</div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-num">{{ stats.records }}</div>
              <div class="stat-label">溯源记录</div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-num">{{ stats.blockHeight }}</div>
              <div class="stat-label">当前区块高度</div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-num">{{ stats.users }}</div>
              <div class="stat-label">注册用户</div>
            </el-card>
          </el-col>
        </el-row>

        <el-card class="quick-trace">
          <template #header>快速溯源查询</template>
          <el-input
            v-model="traceCode"
            placeholder="输入溯源批次号"
            style="max-width: 400px"
          >
            <template #append>
              <el-button @click="goTrace">查询</el-button>
            </template>
          </el-input>
        </el-card>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const activeMenu = computed(() => route.path)
const traceCode = ref('')

const userInfo = computed(() => {
  const info = localStorage.getItem('userInfo')
  return info ? JSON.parse(info) : null
})

const isAdmin = computed(() => userInfo.value?.role === 'admin')

const stats = ref({ batches: 12, records: 48, blockHeight: 2100, users: 5 })

const handleCommand = (cmd: string) => {
  if (cmd === 'logout') {
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
    router.push('/login')
  }
}

const goTrace = () => {
  if (traceCode.value.trim()) {
    router.push(`/trace/${traceCode.value.trim()}`)
  }
}
</script>

<style scoped>
.layout { min-height: 100vh; }
.sidebar { background: #1a3a5c; }
.sidebar-logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  border-bottom: 1px solid #2d5a8e;
}
.header {
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e8e8e8;
  padding: 0 20px;
}
.header-title { font-size: 16px; font-weight: 600; color: #333; }
.header-right { display: flex; align-items: center; gap: 16px; }
.user-info { cursor: pointer; display: flex; align-items: center; gap: 4px; }
.stat-cards { margin-bottom: 16px; }
.stat-card { text-align: center; }
.stat-num { font-size: 32px; font-weight: 700; color: #1a5276; }
.stat-label { color: #888; font-size: 14px; margin-top: 4px; }
.quick-trace { margin-top: 16px; }
</style>
