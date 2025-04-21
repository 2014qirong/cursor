<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>支付方式管理</span>
          <el-button type="primary" @click="handleAddPayment">新增支付方式</el-button>
        </div>
      </template>

      <!-- 支付方式列表 -->
      <el-table
        v-loading="loading"
        :data="paymentList"
        border
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="支付方式名称" width="160" />
        <el-table-column prop="code" label="支付标识" width="120" />
        <el-table-column label="支付图标" width="100" align="center">
          <template #default="scope">
            <el-image
              v-if="scope.row.icon"
              :src="scope.row.icon"
              style="width: 40px; height: 40px"
              fit="contain"
            />
            <el-icon v-else><Money /></el-icon>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="支付说明" min-width="180" />
        <el-table-column prop="fee" label="手续费率" width="100" align="center">
          <template #default="scope">
            {{ scope.row.fee }}%
          </template>
        </el-table-column>
        <el-table-column prop="sort" label="排序" width="80" align="center" />
        <el-table-column label="状态" width="100" align="center">
          <template #default="scope">
            <el-switch
              v-model="scope.row.status"
              :active-value="1"
              :inactive-value="0"
              @change="handleStatusChange(scope.row)"
            />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button
              size="small"
              type="primary"
              link
              @click="handleEdit(scope.row)"
            >
              编辑
            </el-button>
            <el-button
              size="small"
              type="success"
              link
              @click="handleConfigure(scope.row)"
            >
              配置
            </el-button>
            <el-button
              size="small"
              type="danger"
              link
              @click="handleDelete(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑支付方式对话框 -->
    <el-dialog
      :title="dialogType === 'add' ? '新增支付方式' : '编辑支付方式'"
      v-model="dialogVisible"
      width="550px"
    >
      <el-form
        ref="paymentFormRef"
        :model="paymentForm"
        :rules="paymentRules"
        label-width="100px"
      >
        <el-form-item label="支付方式名称" prop="name">
          <el-input v-model="paymentForm.name" placeholder="请输入支付方式名称" />
        </el-form-item>
        <el-form-item label="支付标识" prop="code">
          <el-input 
            v-model="paymentForm.code" 
            placeholder="请输入支付标识"
            :disabled="dialogType === 'edit'"
          />
          <div class="form-help">例如：alipay, wechat, bank_transfer</div>
        </el-form-item>
        <el-form-item label="支付图标">
          <el-upload
            class="avatar-uploader"
            action="#"
            :show-file-list="false"
            :auto-upload="false"
            :on-change="handleIconChange"
          >
            <img v-if="paymentForm.icon" :src="paymentForm.icon" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
          <div class="form-help">建议上传正方形图标，大小不超过200KB</div>
        </el-form-item>
        <el-form-item label="支付说明" prop="description">
          <el-input
            v-model="paymentForm.description"
            type="textarea"
            rows="3"
            placeholder="请输入支付说明文字"
          />
        </el-form-item>
        <el-form-item label="手续费率" prop="fee">
          <el-input-number
            v-model="paymentForm.fee"
            :min="0"
            :max="100"
            :precision="2"
            :step="0.1"
          />
          <span class="ml-2">%</span>
        </el-form-item>
        <el-form-item label="排序" prop="sort">
          <el-input-number v-model="paymentForm.sort" :min="0" :max="999" />
          <div class="form-help">数字越小越靠前</div>
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="paymentForm.status">
            <el-radio :label="1">启用</el-radio>
            <el-radio :label="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitPaymentForm">确定</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 支付方式配置对话框 -->
    <el-dialog
      title="支付方式配置"
      v-model="configDialogVisible"
      width="650px"
    >
      <div v-if="currentPayment.code === 'alipay'">
        <el-form ref="alipayFormRef" label-width="180px">
          <el-form-item label="应用ID(APPID)" required>
            <el-input v-model="configForm.appId" placeholder="请输入支付宝应用ID" />
          </el-form-item>
          <el-form-item label="支付宝公钥" required>
            <el-input 
              v-model="configForm.publicKey"
              type="textarea"
              rows="4"
              placeholder="请输入支付宝公钥"
            />
          </el-form-item>
          <el-form-item label="应用私钥" required>
            <el-input 
              v-model="configForm.privateKey"
              type="textarea"
              rows="4"
              placeholder="请输入应用私钥"
            />
          </el-form-item>
          <el-form-item label="回调地址">
            <el-input v-model="configForm.notifyUrl" placeholder="请输入异步回调地址" />
          </el-form-item>
          <el-form-item label="沙箱模式">
            <el-switch v-model="configForm.sandbox" />
          </el-form-item>
        </el-form>
      </div>
      <div v-else-if="currentPayment.code === 'wechat'">
        <el-form ref="wechatFormRef" label-width="180px">
          <el-form-item label="商户号(MCH_ID)" required>
            <el-input v-model="configForm.mchId" placeholder="请输入微信支付商户号" />
          </el-form-item>
          <el-form-item label="商户API密钥" required>
            <el-input v-model="configForm.mchKey" placeholder="请输入商户API密钥" />
          </el-form-item>
          <el-form-item label="应用ID(APP_ID)" required>
            <el-input v-model="configForm.appId" placeholder="请输入微信支付应用ID" />
          </el-form-item>
          <el-form-item label="应用密钥(APP_SECRET)" required>
            <el-input v-model="configForm.appSecret" placeholder="请输入应用密钥" />
          </el-form-item>
          <el-form-item label="回调地址">
            <el-input v-model="configForm.notifyUrl" placeholder="请输入异步回调地址" />
          </el-form-item>
          <el-form-item label="证书文件(apiclient_cert.p12)">
            <el-upload
              class="upload-demo"
              action="#"
              :auto-upload="false"
              :on-change="handleCertFileChange"
            >
              <el-button type="primary">选择证书文件</el-button>
            </el-upload>
          </el-form-item>
          <el-form-item label="沙箱模式">
            <el-switch v-model="configForm.sandbox" />
          </el-form-item>
        </el-form>
      </div>
      <div v-else>
        <div class="payment-config-placeholder">
          <el-empty description="暂无配置项" />
        </div>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="configDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="savePaymentConfig">保存配置</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Money, Plus } from '@element-plus/icons-vue'

// 加载状态
const loading = ref(false)

// 支付方式列表数据
const paymentList = ref([
  {
    id: 1,
    name: '支付宝',
    code: 'alipay',
    icon: 'https://img.alicdn.com/imgextra/i4/O1CN01XWg0YS1YQIDyQBBvr_!!6000000003050-2-tps-200-200.png',
    description: '支持支付宝APP、扫码、网页支付',
    fee: 0.6,
    sort: 1,
    status: 1
  },
  {
    id: 2,
    name: '微信支付',
    code: 'wechat',
    icon: 'https://res.wx.qq.com/a/wx_fed/assets/res/NTI4MWU5.ico',
    description: '支持微信扫码、公众号、小程序支付',
    fee: 0.6,
    sort: 2,
    status: 1
  },
  {
    id: 3,
    name: '银联支付',
    code: 'unionpay',
    icon: 'https://mdn.alipayobjects.com/huamei_ptpmx/afts/img/A*tQ9VQZ26jgQAAAAAAAAAAAAADvl6AQ/original',
    description: '支持银联卡支付，包括借记卡和信用卡',
    fee: 0.5,
    sort: 3,
    status: 1
  },
  {
    id: 4,
    name: '货到付款',
    code: 'cod',
    icon: null,
    description: '送货上门后现金支付给快递员',
    fee: 0,
    sort: 4,
    status: 1
  },
  {
    id: 5,
    name: '余额支付',
    code: 'balance',
    icon: null,
    description: '使用账户余额支付',
    fee: 0,
    sort: 5,
    status: 1
  }
])

// 支付方式表单相关
const dialogVisible = ref(false)
const dialogType = ref('add') // 'add' or 'edit'
const paymentFormRef = ref(null)
const paymentForm = reactive({
  id: undefined,
  name: '',
  code: '',
  icon: '',
  description: '',
  fee: 0,
  sort: 0,
  status: 1
})

// 支付方式配置相关
const configDialogVisible = ref(false)
const currentPayment = ref({})
const configForm = reactive({
  appId: '',
  mchId: '',
  mchKey: '',
  publicKey: '',
  privateKey: '',
  appSecret: '',
  notifyUrl: 'https://yourdomain.com/api/payment/notify',
  sandbox: false
})

// 支付方式表单验证规则
const paymentRules = {
  name: [
    { required: true, message: '请输入支付方式名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入支付标识', trigger: 'blur' },
    { pattern: /^[a-z][a-z0-9_]*$/, message: '支付标识只能包含小写字母、数字和下划线，并且以字母开头', trigger: 'blur' }
  ],
  description: [
    { max: 200, message: '长度不能超过 200 个字符', trigger: 'blur' }
  ]
}

// 处理添加支付方式
const handleAddPayment = () => {
  dialogType.value = 'add'
  resetPaymentForm()
  dialogVisible.value = true
}

// 处理编辑支付方式
const handleEdit = (row) => {
  dialogType.value = 'edit'
  resetPaymentForm()
  Object.assign(paymentForm, { ...row })
  dialogVisible.value = true
}

// 重置支付方式表单
const resetPaymentForm = () => {
  if (paymentFormRef.value) {
    paymentFormRef.value.resetFields()
  }
  
  Object.assign(paymentForm, {
    id: undefined,
    name: '',
    code: '',
    icon: '',
    description: '',
    fee: 0,
    sort: 0,
    status: 1
  })
}

// 处理图标上传
const handleIconChange = (file) => {
  // 实际项目中应上传到服务器，这里模拟本地预览
  const reader = new FileReader()
  reader.onload = (e) => {
    paymentForm.icon = e.target.result
  }
  reader.readAsDataURL(file.raw)
}

// 处理证书文件上传
const handleCertFileChange = () => {
  ElMessage.success('证书文件已选择，保存后将上传至服务器')
}

// 提交支付方式表单
const submitPaymentForm = () => {
  if (!paymentFormRef.value) return
  
  paymentFormRef.value.validate((valid) => {
    if (valid) {
      if (dialogType.value === 'add') {
        // 新增支付方式
        const newPayment = { ...paymentForm }
        
        // 生成ID
        const maxId = Math.max(...paymentList.value.map(item => item.id), 0)
        newPayment.id = maxId + 1
        
        paymentList.value.push(newPayment)
        ElMessage.success('新增支付方式成功')
      } else {
        // 编辑支付方式
        const index = paymentList.value.findIndex(item => item.id === paymentForm.id)
        if (index !== -1) {
          paymentList.value[index] = { ...paymentList.value[index], ...paymentForm }
          ElMessage.success('修改支付方式成功')
        }
      }
      
      dialogVisible.value = false
    }
  })
}

// 处理支付方式状态变更
const handleStatusChange = (row) => {
  const statusText = row.status === 1 ? '启用' : '禁用'
  ElMessage.success(`已${statusText}支付方式：${row.name}`)
  
  // 实际应用中应调用API更新状态
  console.log('状态变更:', row)
}

// 处理删除支付方式
const handleDelete = (row) => {
  ElMessageBox.confirm(`确认删除支付方式 ${row.name} 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    const index = paymentList.value.findIndex(item => item.id === row.id)
    if (index !== -1) {
      paymentList.value.splice(index, 1)
      ElMessage.success('删除支付方式成功')
    }
  }).catch(() => {})
}

// 处理配置支付方式
const handleConfigure = (row) => {
  currentPayment.value = { ...row }
  configDialogVisible.value = true
  
  // 模拟获取支付方式配置
  // 实际应该调用API获取配置
  resetConfigForm()
  
  if (row.code === 'alipay') {
    Object.assign(configForm, {
      appId: '2016xxxxxxxx',
      publicKey: 'MIIBIjANBgkqhkiG9w0BAQEF...',
      privateKey: 'MIIEvQIBADANBgkqhkiG9w0BAQEF...',
      notifyUrl: 'https://yourdomain.com/api/payment/alipay/notify',
      sandbox: true
    })
  } else if (row.code === 'wechat') {
    Object.assign(configForm, {
      mchId: '1900xxxxxx',
      mchKey: 'xxxxxxxxxxxxxxxxx',
      appId: 'wxxxxxxxxxxx',
      appSecret: 'xxxxxxxxxxxxxx',
      notifyUrl: 'https://yourdomain.com/api/payment/wechat/notify',
      sandbox: true
    })
  }
}

// 重置配置表单
const resetConfigForm = () => {
  Object.assign(configForm, {
    appId: '',
    mchId: '',
    mchKey: '',
    publicKey: '',
    privateKey: '',
    appSecret: '',
    notifyUrl: 'https://yourdomain.com/api/payment/notify',
    sandbox: false
  })
}

// 保存支付方式配置
const savePaymentConfig = () => {
  ElMessage.success(`保存 ${currentPayment.value.name} 支付配置成功`)
  configDialogVisible.value = false
  
  // 实际应用中应调用API保存配置
  console.log('保存支付配置:', currentPayment.value.code, configForm)
}

onMounted(() => {
  // 获取支付方式列表
  loading.value = true
  setTimeout(() => {
    loading.value = false
  }, 300)
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

.form-help {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.ml-2 {
  margin-left: 8px;
}

.avatar-uploader {
  .avatar {
    width: 80px;
    height: 80px;
    display: block;
    object-fit: contain;
    border: 1px dashed #d9d9d9;
    border-radius: 4px;
  }
  
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 80px;
    height: 80px;
    line-height: 80px;
    text-align: center;
    border: 1px dashed #d9d9d9;
    border-radius: 4px;
  }
}

.payment-config-placeholder {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style> 