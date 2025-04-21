<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>短信配置</span>
        </div>
      </template>
      
      <el-tabs v-model="activeTab">
        <el-tab-pane label="短信服务配置" name="config">
          <el-form
            ref="configFormRef"
            :model="configForm"
            :rules="configRules"
            label-width="120px"
          >
            <el-form-item label="短信服务商" prop="provider">
              <el-select v-model="configForm.provider" placeholder="请选择短信服务商">
                <el-option label="阿里云" value="aliyun" />
                <el-option label="腾讯云" value="tencent" />
                <el-option label="七牛云" value="qiniu" />
              </el-select>
            </el-form-item>
            
            <template v-if="configForm.provider === 'aliyun'">
              <el-form-item label="AccessKey ID" prop="accessKeyId">
                <el-input v-model="configForm.accessKeyId" placeholder="请输入AccessKey ID" />
              </el-form-item>
              <el-form-item label="AccessKey Secret" prop="accessKeySecret">
                <el-input v-model="configForm.accessKeySecret" placeholder="请输入AccessKey Secret" show-password />
              </el-form-item>
              <el-form-item label="签名" prop="signName">
                <el-input v-model="configForm.signName" placeholder="请输入短信签名" />
              </el-form-item>
              <el-form-item label="区域" prop="region">
                <el-input v-model="configForm.region" placeholder="请输入区域，例如：cn-hangzhou" />
              </el-form-item>
            </template>
            
            <template v-if="configForm.provider === 'tencent'">
              <el-form-item label="SecretId" prop="secretId">
                <el-input v-model="configForm.secretId" placeholder="请输入SecretId" />
              </el-form-item>
              <el-form-item label="SecretKey" prop="secretKey">
                <el-input v-model="configForm.secretKey" placeholder="请输入SecretKey" show-password />
              </el-form-item>
              <el-form-item label="短信AppID" prop="appId">
                <el-input v-model="configForm.appId" placeholder="请输入AppID" />
              </el-form-item>
              <el-form-item label="签名" prop="signName">
                <el-input v-model="configForm.signName" placeholder="请输入短信签名" />
              </el-form-item>
            </template>
            
            <template v-if="configForm.provider === 'qiniu'">
              <el-form-item label="AccessKey" prop="accessKey">
                <el-input v-model="configForm.accessKey" placeholder="请输入AccessKey" />
              </el-form-item>
              <el-form-item label="SecretKey" prop="secretKey">
                <el-input v-model="configForm.secretKey" placeholder="请输入SecretKey" show-password />
              </el-form-item>
              <el-form-item label="签名" prop="signName">
                <el-input v-model="configForm.signName" placeholder="请输入短信签名" />
              </el-form-item>
            </template>
            
            <el-form-item>
              <el-button type="primary" @click="saveConfig">保存配置</el-button>
              <el-button @click="testSms">测试发送</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="短信模板设置" name="template">
          <el-table
            v-loading="listLoading"
            :data="templateList"
            border
            style="width: 100%"
          >
            <el-table-column label="场景" prop="scene" min-width="120">
              <template #default="scope">
                {{ getSceneName(scope.row.scene) }}
              </template>
            </el-table-column>
            <el-table-column label="模板ID" prop="templateId" min-width="180" />
            <el-table-column label="模板内容" prop="content" min-width="250" show-overflow-tooltip />
            <el-table-column label="状态" width="100" align="center">
              <template #default="scope">
                <el-tag :type="scope.row.status === 1 ? 'success' : 'info'">
                  {{ scope.row.status === 1 ? '启用' : '禁用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="scope">
                <el-button 
                  size="small" 
                  type="primary" 
                  link 
                  @click="handleEditTemplate(scope.row)"
                >
                  编辑
                </el-button>
                <el-button 
                  size="small" 
                  :type="scope.row.status === 0 ? 'success' : 'warning'" 
                  link 
                  @click="handleToggleStatus(scope.row)"
                >
                  {{ scope.row.status === 0 ? '启用' : '禁用' }}
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        
        <el-tab-pane label="发送记录" name="log">
          <div class="filter-container">
            <el-form :inline="true" :model="logQuery" @keyup.enter="fetchLogs">
              <el-form-item label="手机号">
                <el-input v-model="logQuery.mobile" placeholder="请输入手机号" clearable />
              </el-form-item>
              <el-form-item label="发送状态">
                <el-select v-model="logQuery.status" placeholder="全部" clearable>
                  <el-option label="成功" :value="1" />
                  <el-option label="失败" :value="0" />
                </el-select>
              </el-form-item>
              <el-form-item label="发送时间">
                <el-date-picker
                  v-model="dateRange"
                  type="daterange"
                  range-separator="至"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                  format="YYYY-MM-DD"
                  value-format="YYYY-MM-DD"
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="fetchLogs">查询</el-button>
                <el-button @click="resetQuery">重置</el-button>
              </el-form-item>
            </el-form>
          </div>
          
          <el-table
            v-loading="logLoading"
            :data="logList"
            border
            style="width: 100%"
          >
            <el-table-column label="ID" prop="id" width="80" align="center" />
            <el-table-column label="手机号" prop="mobile" width="120" />
            <el-table-column label="场景" prop="scene" width="120">
              <template #default="scope">
                {{ getSceneName(scope.row.scene) }}
              </template>
            </el-table-column>
            <el-table-column label="内容" prop="content" min-width="250" show-overflow-tooltip />
            <el-table-column label="发送时间" prop="sendTime" width="180" />
            <el-table-column label="状态" width="100" align="center">
              <template #default="scope">
                <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'">
                  {{ scope.row.status === 1 ? '成功' : '失败' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="备注" prop="remark" min-width="180" show-overflow-tooltip />
          </el-table>
          
          <pagination
            v-show="logTotal > 0"
            :total="logTotal"
            v-model:page="logQuery.page"
            v-model:limit="logQuery.limit"
            @pagination="fetchLogs"
          />
        </el-tab-pane>
      </el-tabs>
    </el-card>
    
    <!-- 短信模板编辑对话框 -->
    <el-dialog
      title="编辑短信模板"
      v-model="dialogFormVisible"
      width="500px"
    >
      <el-form
        ref="templateFormRef"
        :model="templateForm"
        :rules="templateRules"
        label-width="100px"
      >
        <el-form-item label="场景" prop="scene">
          <el-select v-model="templateForm.scene" placeholder="请选择短信场景" disabled>
            <el-option
              v-for="item in sceneOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="模板ID" prop="templateId">
          <el-input v-model="templateForm.templateId" placeholder="请输入模板ID" />
        </el-form-item>
        <el-form-item label="模板内容" prop="content">
          <el-input
            v-model="templateForm.content"
            type="textarea"
            rows="4"
            placeholder="请输入模板内容"
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="templateForm.status">
            <el-radio :label="1">启用</el-radio>
            <el-radio :label="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取消</el-button>
          <el-button type="primary" @click="submitTemplateForm">确定</el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- 短信测试对话框 -->
    <el-dialog
      title="测试短信发送"
      v-model="testDialogVisible"
      width="400px"
    >
      <el-form
        ref="testFormRef"
        :model="testForm"
        :rules="testRules"
        label-width="80px"
      >
        <el-form-item label="手机号" prop="mobile">
          <el-input v-model="testForm.mobile" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="场景" prop="scene">
          <el-select v-model="testForm.scene" placeholder="请选择短信场景">
            <el-option
              v-for="item in sceneOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="testDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitTestForm">发送测试</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import Pagination from '@/components/Pagination/index.vue'

// 当前活跃选项卡
const activeTab = ref('config')

// 短信服务配置表单
const configFormRef = ref(null)
const configForm = reactive({
  provider: 'aliyun',
  accessKeyId: '',
  accessKeySecret: '',
  secretId: '',
  secretKey: '',
  appId: '',
  accessKey: '',
  signName: '',
  region: 'cn-hangzhou'
})

// 配置表单规则
const configRules = {
  provider: [
    { required: true, message: '请选择短信服务商', trigger: 'change' }
  ],
  accessKeyId: [
    { required: true, message: '请输入AccessKey ID', trigger: 'blur' }
  ],
  accessKeySecret: [
    { required: true, message: '请输入AccessKey Secret', trigger: 'blur' }
  ],
  secretId: [
    { required: true, message: '请输入SecretId', trigger: 'blur' }
  ],
  secretKey: [
    { required: true, message: '请输入SecretKey', trigger: 'blur' }
  ],
  appId: [
    { required: true, message: '请输入AppID', trigger: 'blur' }
  ],
  accessKey: [
    { required: true, message: '请输入AccessKey', trigger: 'blur' }
  ],
  signName: [
    { required: true, message: '请输入短信签名', trigger: 'blur' }
  ]
}

// 模板列表
const listLoading = ref(false)
const templateList = ref([
  {
    id: 1,
    scene: 'register',
    templateId: 'SMS_123456789',
    content: '验证码：${code}，您正在注册成为新用户，感谢您的支持！',
    status: 1
  },
  {
    id: 2,
    scene: 'login',
    templateId: 'SMS_987654321',
    content: '验证码：${code}，您正在登录，若非本人操作，请忽略本短信。',
    status: 1
  },
  {
    id: 3,
    scene: 'resetPassword',
    templateId: 'SMS_456789123',
    content: '验证码：${code}，您正在进行密码重置操作，请妥善保管验证码。',
    status: 1
  },
  {
    id: 4,
    scene: 'orderPay',
    templateId: 'SMS_789123456',
    content: '您的订单${orderNo}已支付成功，我们将尽快为您安排发货。',
    status: 1
  },
  {
    id: 5,
    scene: 'orderShip',
    templateId: 'SMS_321654987',
    content: '您的订单${orderNo}已发货，物流单号：${trackingNo}，请注意查收。',
    status: 1
  },
  {
    id: 6,
    scene: 'coupon',
    templateId: 'SMS_654987321',
    content: '您有一张${amount}元优惠券已到账，有效期至${expireTime}，请尽快使用。',
    status: 0
  }
])

// 短信模板编辑对话框
const dialogFormVisible = ref(false)
const templateFormRef = ref(null)
const templateForm = reactive({
  id: undefined,
  scene: '',
  templateId: '',
  content: '',
  status: 1
})

// 模板表单规则
const templateRules = {
  templateId: [
    { required: true, message: '请输入模板ID', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入模板内容', trigger: 'blur' }
  ]
}

// 短信测试对话框
const testDialogVisible = ref(false)
const testFormRef = ref(null)
const testForm = reactive({
  mobile: '',
  scene: ''
})

// 测试表单规则
const testRules = {
  mobile: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3456789]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  scene: [
    { required: true, message: '请选择短信场景', trigger: 'change' }
  ]
}

// 短信发送记录查询
const logLoading = ref(false)
const logTotal = ref(0)
const logList = ref([])
const dateRange = ref([])
const logQuery = reactive({
  page: 1,
  limit: 10,
  mobile: '',
  status: '',
  startDate: '',
  endDate: ''
})

// 场景选项
const sceneOptions = [
  { label: '注册验证', value: 'register' },
  { label: '登录验证', value: 'login' },
  { label: '密码重置', value: 'resetPassword' },
  { label: '订单支付通知', value: 'orderPay' },
  { label: '订单发货通知', value: 'orderShip' },
  { label: '优惠券到账通知', value: 'coupon' }
]

// 监听日期范围变化
watch(dateRange, (val) => {
  if (val) {
    logQuery.startDate = val[0]
    logQuery.endDate = val[1]
  } else {
    logQuery.startDate = ''
    logQuery.endDate = ''
  }
})

// 获取场景名称
const getSceneName = (scene) => {
  const option = sceneOptions.find(item => item.value === scene)
  return option ? option.label : scene
}

// 保存短信配置
const saveConfig = () => {
  if (!configFormRef.value) return
  
  configFormRef.value.validate((valid) => {
    if (valid) {
      // 模拟API请求
      console.log('保存短信配置:', configForm)
      ElMessage.success('短信配置保存成功')
    }
  })
}

// 测试短信发送
const testSms = () => {
  testForm.mobile = ''
  testForm.scene = ''
  testDialogVisible.value = true
}

// 提交测试表单
const submitTestForm = () => {
  if (!testFormRef.value) return
  
  testFormRef.value.validate((valid) => {
    if (valid) {
      // 模拟API请求
      ElMessage.success(`测试短信已发送至 ${testForm.mobile}`)
      testDialogVisible.value = false
      
      // 添加到发送记录
      const template = templateList.value.find(item => item.scene === testForm.scene)
      if (template) {
        logList.value.unshift({
          id: Date.now(),
          mobile: testForm.mobile,
          scene: testForm.scene,
          content: template.content.replace('${code}', '123456'),
          sendTime: new Date().toLocaleString(),
          status: 1,
          remark: '测试发送'
        })
      }
    }
  })
}

// 编辑短信模板
const handleEditTemplate = (row) => {
  Object.assign(templateForm, { ...row })
  dialogFormVisible.value = true
}

// 提交模板表单
const submitTemplateForm = () => {
  if (!templateFormRef.value) return
  
  templateFormRef.value.validate((valid) => {
    if (valid) {
      const index = templateList.value.findIndex(item => item.id === templateForm.id)
      if (index !== -1) {
        templateList.value[index] = { ...templateForm }
        ElMessage.success('模板更新成功')
        dialogFormVisible.value = false
      }
    }
  })
}

// 切换模板状态
const handleToggleStatus = (row) => {
  const newStatus = row.status === 1 ? 0 : 1
  const statusText = newStatus === 1 ? '启用' : '禁用'
  
  ElMessageBox.confirm(
    `确定要${statusText}该短信模板吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    const index = templateList.value.findIndex(item => item.id === row.id)
    if (index !== -1) {
      templateList.value[index].status = newStatus
      ElMessage.success(`${statusText}成功`)
    }
  }).catch(() => {})
}

// 获取短信发送记录
const fetchLogs = () => {
  logLoading.value = true
  
  // 模拟API请求
  setTimeout(() => {
    // 生成测试数据
    logList.value = []
    for (let i = 0; i < 10; i++) {
      const scene = sceneOptions[Math.floor(Math.random() * sceneOptions.length)].value
      const status = Math.random() > 0.2 ? 1 : 0
      const date = new Date()
      date.setDate(date.getDate() - Math.floor(Math.random() * 7))
      
      logList.value.push({
        id: 1000 + i,
        mobile: `1${Math.floor(Math.random() * 9 + 3)}${Array(9).fill(0).map(() => Math.floor(Math.random() * 10)).join('')}`,
        scene,
        content: templateList.value.find(t => t.scene === scene)?.content.replace('${code}', Math.floor(100000 + Math.random() * 900000)),
        sendTime: date.toLocaleString(),
        status,
        remark: status ? '发送成功' : '运营商网络异常'
      })
    }
    
    logTotal.value = 35
    logLoading.value = false
  }, 500)
}

// 重置查询条件
const resetQuery = () => {
  logQuery.mobile = ''
  logQuery.status = ''
  dateRange.value = []
  logQuery.startDate = ''
  logQuery.endDate = ''
  fetchLogs()
}

// 获取短信配置
const getConfig = () => {
  // 模拟API请求
  setTimeout(() => {
    Object.assign(configForm, {
      provider: 'aliyun',
      accessKeyId: 'LTAI4GxxxxxxxxxxxxxxxxPN',
      accessKeySecret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
      signName: '商城',
      region: 'cn-hangzhou'
    })
  }, 300)
}

onMounted(() => {
  getConfig()
  fetchLogs()
})
</script>

<style lang="scss" scoped>
.app-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-container {
  margin-bottom: 20px;
}
</style> 