<template>
  <el-container class="layout">
    <el-aside width="220px" class="sidebar">
      <div class="sidebar-logo">🌾 农产品溯源系统</div>
      <el-menu router background-color="#1a3a5c" text-color="#c0d8f0" active-text-color="#ffffff">
        <el-menu-item index="/dashboard"><el-icon><DataBoard /></el-icon><span>系统概览</span></el-menu-item>
        <el-menu-item index="/batches"><el-icon><Box /></el-icon><span>批次管理</span></el-menu-item>
        <el-menu-item index="/trace-records"><el-icon><List /></el-icon><span>溯源记录</span></el-menu-item>
        <el-menu-item index="/admin/users"><el-icon><User /></el-icon><span>用户管理</span></el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <span class="header-title">用户管理</span>
        <el-button type="primary" @click="showReg = true">新增用户</el-button>
      </el-header>
      <el-main>
        <el-table :data="users" stripe border>
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="username" label="账号" width="120" />
          <el-table-column prop="real_name" label="姓名/企业" width="160" />
          <el-table-column prop="role" label="角色" width="100">
            <template #default="{ row }">
              <el-tag :type="roleType(row.role)">{{ roleLabel(row.role) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="phone" label="联系电话" width="140" />
          <el-table-column prop="created_at" label="注册时间" min-width="160" />
        </el-table>
      </el-main>
    </el-container>
  </el-container>

  <el-dialog v-model="showReg" title="新增用户" width="480px">
    <el-form :model="regForm" label-width="100px">
      <el-form-item label="账号"><el-input v-model="regForm.username" /></el-form-item>
      <el-form-item label="密码"><el-input v-model="regForm.password" type="password" /></el-form-item>
      <el-form-item label="姓名/企业"><el-input v-model="regForm.real_name" /></el-form-item>
      <el-form-item label="角色">
        <el-select v-model="regForm.role">
          <el-option label="种植户" value="farmer" />
          <el-option label="质检员" value="inspector" />
          <el-option label="物流商" value="transporter" />
          <el-option label="销售商" value="retailer" />
        </el-select>
      </el-form-item>
      <el-form-item label="联系电话"><el-input v-model="regForm.phone" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="showReg = false">取消</el-button>
      <el-button type="primary" @click="doReg">确认</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { register } from '../../api/trace'

const users = ref<any[]>([])
const showReg = ref(false)
const regForm = ref({ username: '', password: '', real_name: '', role: 'farmer', phone: '' })

const roleLabel = (r: string) => ({ admin: '管理员', farmer: '种植户', inspector: '质检员', transporter: '物流商', retailer: '销售商' }[r] || r)
const roleType = (r: string) => ({ admin: 'danger', farmer: 'success', inspector: 'primary', transporter: 'info', retailer: 'warning' }[r] || '')

const doReg = async () => {
  try {
    await register(regForm.value)
    ElMessage.success('用户创建成功')
    showReg.value = false
  } catch {}
}

onMounted(() => {
  // 实际项目中调用 listUsers 接口
  users.value = [
    { id: 1, username: 'admin', real_name: '系统管理员', role: 'admin', phone: '13800000000', created_at: '2025-01-01' },
    { id: 2, username: 'farmer01', real_name: '张三果园专业合作社', role: 'farmer', phone: '13800000001', created_at: '2025-01-02' },
    { id: 3, username: 'inspector01', real_name: '农产品质量检测中心-李四', role: 'inspector', phone: '13800000002', created_at: '2025-01-03' },
  ]
})
</script>

<style scoped>
.layout { min-height: 100vh; }
.sidebar { background: #1a3a5c; }
.sidebar-logo { height: 60px; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 15px; font-weight: 600; border-bottom: 1px solid #2d5a8e; }
.header { background: #fff; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #e8e8e8; padding: 0 20px; }
.header-title { font-size: 16px; font-weight: 600; color: #333; }
</style>
