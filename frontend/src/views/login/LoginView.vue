<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <!-- <img src="/logo.png" alt="logo" class="logo" /> -->
        <h1>农产品溯源管理系统</h1>
        <p>基于国密区块链 · Hyperledger Fabric</p>
      </div>
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <el-button
          type="primary"
          size="large"
          class="login-btn"
          :loading="loading"
          @click="handleLogin"
        >
          登 录
        </el-button>
      </el-form>
      <div class="login-footer">
        <span>溯源查询（无需登录）：</span>
        <el-input
          v-model="traceCode"
          placeholder="输入溯源码"
          style="width: 200px; margin: 0 8px"
          size="small"
        />
        <el-button size="small" type="success" @click="goTrace">查询</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login } from '../../api/trace'

const router = useRouter()
const formRef = ref()
const loading = ref(false)
const traceCode = ref('')

const form = reactive({ username: '', password: '' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

const handleLogin = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid: boolean) => {
    if (!valid) return
    loading.value = true
    try {
      const data: any = await login(form)
      localStorage.setItem('token', data.token)
      localStorage.setItem('userInfo', JSON.stringify(data))
      ElMessage.success('登录成功')
      router.push('/dashboard')
    } catch (e) {
      // 错误已在拦截器处理
    } finally {
      loading.value = false
    }
  })
}

const goTrace = () => {
  if (!traceCode.value.trim()) {
    ElMessage.warning('请输入溯源码')
    return
  }
  router.push(`/trace/${traceCode.value.trim()}`)
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a5276 0%, #27ae60 100%);
}
.login-card {
  width: 420px;
  background: #fff;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}
.login-header {
  text-align: center;
  margin-bottom: 32px;
}
.logo {
  width: 64px;
  height: 64px;
  margin-bottom: 12px;
}
.login-header h1 {
  font-size: 22px;
  color: #1a5276;
  font-weight: 700;
  margin-bottom: 6px;
}
.login-header p {
  font-size: 13px;
  color: #888;
}
.login-btn {
  width: 100%;
  margin-top: 8px;
}
.login-footer {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
  font-size: 13px;
  color: #666;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 4px;
}
</style>
