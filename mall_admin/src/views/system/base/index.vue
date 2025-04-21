<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>基础设置</span>
        </div>
      </template>
      
      <el-tabs v-model="activeName">
        <el-tab-pane label="网站信息" name="site">
          <el-form
            ref="siteFormRef"
            :model="siteForm"
            :rules="siteRules"
            label-width="100px"
            class="setting-form"
          >
            <el-form-item label="网站名称" prop="siteName">
              <el-input v-model="siteForm.siteName" placeholder="请输入网站名称" />
            </el-form-item>
            
            <el-form-item label="网站LOGO">
              <el-upload
                class="avatar-uploader"
                action="/api/upload"
                :show-file-list="false"
                :on-success="handleLogoSuccess"
                :before-upload="beforeLogoUpload"
              >
                <img v-if="siteForm.logo" :src="siteForm.logo" class="avatar" />
                <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
              </el-upload>
            </el-form-item>
            
            <el-form-item label="网站描述" prop="description">
              <el-input 
                v-model="siteForm.description" 
                type="textarea" 
                rows="4" 
                placeholder="请输入网站描述"
              />
            </el-form-item>
            
            <el-form-item label="客服电话" prop="servicePhone">
              <el-input v-model="siteForm.servicePhone" placeholder="请输入客服电话" />
            </el-form-item>
            
            <el-form-item label="客服邮箱" prop="serviceEmail">
              <el-input v-model="siteForm.serviceEmail" placeholder="请输入客服邮箱" />
            </el-form-item>
            
            <el-form-item label="备案信息" prop="icp">
              <el-input v-model="siteForm.icp" placeholder="请输入备案信息" />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveSiteInfo">保存设置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="微信设置" name="wechat">
          <el-form
            ref="wechatFormRef"
            :model="wechatForm"
            :rules="wechatRules"
            label-width="120px"
            class="setting-form"
          >
            <el-form-item label="小程序AppID" prop="appId">
              <el-input v-model="wechatForm.appId" placeholder="请输入小程序AppID" />
            </el-form-item>
            
            <el-form-item label="小程序AppSecret" prop="appSecret">
              <el-input v-model="wechatForm.appSecret" placeholder="请输入小程序AppSecret" show-password />
            </el-form-item>
            
            <el-form-item label="公众号AppID" prop="mpAppId">
              <el-input v-model="wechatForm.mpAppId" placeholder="请输入公众号AppID" />
            </el-form-item>
            
            <el-form-item label="公众号AppSecret" prop="mpAppSecret">
              <el-input v-model="wechatForm.mpAppSecret" placeholder="请输入公众号AppSecret" show-password />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveWechatInfo">保存设置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="上传设置" name="upload">
          <el-form
            ref="uploadFormRef"
            :model="uploadForm"
            label-width="120px"
            class="setting-form"
          >
            <el-form-item label="存储方式">
              <el-radio-group v-model="uploadForm.storageType">
                <el-radio label="local">本地存储</el-radio>
                <el-radio label="oss">阿里云OSS</el-radio>
                <el-radio label="cos">腾讯云COS</el-radio>
                <el-radio label="qiniu">七牛云</el-radio>
              </el-radio-group>
            </el-form-item>
            
            <template v-if="uploadForm.storageType === 'local'">
              <el-form-item label="上传目录">
                <el-input v-model="uploadForm.uploadDir" placeholder="请输入上传目录" />
              </el-form-item>
            </template>
            
            <template v-if="uploadForm.storageType === 'oss'">
              <el-form-item label="AccessKey ID">
                <el-input v-model="uploadForm.ossAccessKeyId" placeholder="请输入AccessKey ID" />
              </el-form-item>
              <el-form-item label="AccessKey Secret">
                <el-input v-model="uploadForm.ossAccessKeySecret" placeholder="请输入AccessKey Secret" show-password />
              </el-form-item>
              <el-form-item label="Bucket">
                <el-input v-model="uploadForm.ossBucket" placeholder="请输入Bucket" />
              </el-form-item>
              <el-form-item label="区域">
                <el-input v-model="uploadForm.ossRegion" placeholder="请输入区域，例如：oss-cn-hangzhou" />
              </el-form-item>
              <el-form-item label="域名">
                <el-input v-model="uploadForm.ossDomain" placeholder="请输入域名" />
              </el-form-item>
            </template>
            
            <template v-if="uploadForm.storageType === 'cos'">
              <el-form-item label="SecretId">
                <el-input v-model="uploadForm.cosSecretId" placeholder="请输入SecretId" />
              </el-form-item>
              <el-form-item label="SecretKey">
                <el-input v-model="uploadForm.cosSecretKey" placeholder="请输入SecretKey" show-password />
              </el-form-item>
              <el-form-item label="Bucket">
                <el-input v-model="uploadForm.cosBucket" placeholder="请输入Bucket" />
              </el-form-item>
              <el-form-item label="区域">
                <el-input v-model="uploadForm.cosRegion" placeholder="请输入区域，例如：ap-guangzhou" />
              </el-form-item>
              <el-form-item label="域名">
                <el-input v-model="uploadForm.cosDomain" placeholder="请输入域名" />
              </el-form-item>
            </template>
            
            <template v-if="uploadForm.storageType === 'qiniu'">
              <el-form-item label="AccessKey">
                <el-input v-model="uploadForm.qiniuAccessKey" placeholder="请输入AccessKey" />
              </el-form-item>
              <el-form-item label="SecretKey">
                <el-input v-model="uploadForm.qiniuSecretKey" placeholder="请输入SecretKey" show-password />
              </el-form-item>
              <el-form-item label="Bucket">
                <el-input v-model="uploadForm.qiniuBucket" placeholder="请输入Bucket" />
              </el-form-item>
              <el-form-item label="区域">
                <el-select v-model="uploadForm.qiniuRegion" placeholder="请选择区域">
                  <el-option label="华东" value="z0" />
                  <el-option label="华北" value="z1" />
                  <el-option label="华南" value="z2" />
                  <el-option label="北美" value="na0" />
                  <el-option label="东南亚" value="as0" />
                </el-select>
              </el-form-item>
              <el-form-item label="域名">
                <el-input v-model="uploadForm.qiniuDomain" placeholder="请输入域名" />
              </el-form-item>
            </template>
            
            <el-form-item label="图片压缩">
              <el-switch
                v-model="uploadForm.imageCompress"
                :active-value="1"
                :inactive-value="0"
              />
            </el-form-item>
            
            <el-form-item label="水印">
              <el-switch
                v-model="uploadForm.watermark"
                :active-value="1"
                :inactive-value="0"
              />
            </el-form-item>
            
            <el-form-item label="水印图片" v-if="uploadForm.watermark === 1">
              <el-upload
                class="avatar-uploader"
                action="/api/upload"
                :show-file-list="false"
                :on-success="handleWatermarkSuccess"
                :before-upload="beforeLogoUpload"
              >
                <img v-if="uploadForm.watermarkImage" :src="uploadForm.watermarkImage" class="avatar" />
                <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
              </el-upload>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveUploadInfo">保存设置</el-button>
              <el-button @click="testUpload">测试上传</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="商城设置" name="shop">
          <el-form
            ref="shopFormRef"
            :model="shopForm"
            label-width="140px"
            class="setting-form"
          >
            <el-form-item label="自动确认收货天数">
              <el-input-number v-model="shopForm.autoReceiveDays" :min="1" :max="30" />
              <span class="form-help">天</span>
            </el-form-item>
            
            <el-form-item label="自动好评天数">
              <el-input-number v-model="shopForm.autoCommentDays" :min="1" :max="30" />
              <span class="form-help">天</span>
            </el-form-item>
            
            <el-form-item label="售后服务期限">
              <el-input-number v-model="shopForm.afterSaleDays" :min="1" :max="30" />
              <span class="form-help">天</span>
            </el-form-item>
            
            <el-form-item label="分销功能">
              <el-switch
                v-model="shopForm.distribution"
                :active-value="1"
                :inactive-value="0"
              />
            </el-form-item>
            
            <el-form-item label="积分功能">
              <el-switch
                v-model="shopForm.pointsEnabled"
                :active-value="1"
                :inactive-value="0"
              />
            </el-form-item>
            
            <el-form-item label="积分兑换比例" v-if="shopForm.pointsEnabled === 1">
              <el-input-number v-model="shopForm.pointsRatio" :min="0.01" :max="100" :precision="2" :step="0.1" />
              <span class="form-help">元 = 1积分</span>
            </el-form-item>
            
            <el-form-item label="注册赠送积分" v-if="shopForm.pointsEnabled === 1">
              <el-input-number v-model="shopForm.registerPoints" :min="0" :max="1000" />
              <span class="form-help">积分</span>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveShopInfo">保存设置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

// 当前活跃选项卡
const activeName = ref('site')

// 网站信息表单
const siteFormRef = ref(null)
const siteForm = reactive({
  siteName: '',
  logo: '',
  description: '',
  servicePhone: '',
  serviceEmail: '',
  icp: ''
})

// 网站信息表单规则
const siteRules = {
  siteName: [
    { required: true, message: '请输入网站名称', trigger: 'blur' }
  ],
  servicePhone: [
    { pattern: /^1[3456789]\d{9}$|^(\(\d{3,4}\)|\d{3,4}-|\s)?\d{7,14}$/, message: '请输入正确的电话号码', trigger: 'blur' }
  ],
  serviceEmail: [
    { pattern: /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/, message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

// 微信设置表单
const wechatFormRef = ref(null)
const wechatForm = reactive({
  appId: '',
  appSecret: '',
  mpAppId: '',
  mpAppSecret: ''
})

// 微信设置表单规则
const wechatRules = {
  appId: [
    { required: true, message: '请输入小程序AppID', trigger: 'blur' }
  ],
  appSecret: [
    { required: true, message: '请输入小程序AppSecret', trigger: 'blur' }
  ]
}

// 上传设置表单
const uploadFormRef = ref(null)
const uploadForm = reactive({
  storageType: 'local',
  uploadDir: 'uploads',
  ossAccessKeyId: '',
  ossAccessKeySecret: '',
  ossBucket: '',
  ossRegion: '',
  ossDomain: '',
  cosSecretId: '',
  cosSecretKey: '',
  cosBucket: '',
  cosRegion: '',
  cosDomain: '',
  qiniuAccessKey: '',
  qiniuSecretKey: '',
  qiniuBucket: '',
  qiniuRegion: 'z0',
  qiniuDomain: '',
  imageCompress: 1,
  watermark: 0,
  watermarkImage: ''
})

// 商城设置表单
const shopFormRef = ref(null)
const shopForm = reactive({
  autoReceiveDays: 7,
  autoCommentDays: 7,
  afterSaleDays: 15,
  distribution: 0,
  pointsEnabled: 1,
  pointsRatio: 1,
  registerPoints: 100
})

// 处理Logo上传成功
const handleLogoSuccess = (res) => {
  siteForm.logo = res.data.url
}

// 处理水印图片上传成功
const handleWatermarkSuccess = (res) => {
  uploadForm.watermarkImage = res.data.url
}

// 上传前的图片检查
const beforeLogoUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('上传文件只能是图片!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('上传图片大小不能超过2MB!')
    return false
  }
  return true
}

// 获取网站信息
const getSiteInfo = () => {
  // 模拟API获取数据
  setTimeout(() => {
    Object.assign(siteForm, {
      siteName: '商城小程序',
      logo: 'https://picsum.photos/200/200?random=1',
      description: '商城小程序是一个综合性的电商平台，提供各类商品的在线购买服务。',
      servicePhone: '400-123-4567',
      serviceEmail: 'service@example.com',
      icp: '粤ICP备12345678号'
    })
  }, 300)
}

// 获取微信设置
const getWechatInfo = () => {
  // 模拟API获取数据
  setTimeout(() => {
    Object.assign(wechatForm, {
      appId: 'wx1234567890abcdef',
      appSecret: 'abcdef1234567890abcdef1234567890',
      mpAppId: 'wx0987654321fedcba',
      mpAppSecret: 'abcdef0987654321abcdef0987654321'
    })
  }, 300)
}

// 获取上传设置
const getUploadInfo = () => {
  // 模拟API获取数据
  setTimeout(() => {
    Object.assign(uploadForm, {
      storageType: 'local',
      uploadDir: 'uploads',
      imageCompress: 1,
      watermark: 0
    })
  }, 300)
}

// 获取商城设置
const getShopInfo = () => {
  // 模拟API获取数据
  setTimeout(() => {
    Object.assign(shopForm, {
      autoReceiveDays: 7,
      autoCommentDays: 7,
      afterSaleDays: 15,
      distribution: 0,
      pointsEnabled: 1,
      pointsRatio: 1,
      registerPoints: 100
    })
  }, 300)
}

// 保存网站信息
const saveSiteInfo = () => {
  if (!siteFormRef.value) return
  
  siteFormRef.value.validate((valid) => {
    if (valid) {
      // 模拟API保存数据
      console.log('保存网站信息:', siteForm)
      ElMessage.success('网站信息保存成功')
    }
  })
}

// 保存微信设置
const saveWechatInfo = () => {
  if (!wechatFormRef.value) return
  
  wechatFormRef.value.validate((valid) => {
    if (valid) {
      // 模拟API保存数据
      console.log('保存微信设置:', wechatForm)
      ElMessage.success('微信设置保存成功')
    }
  })
}

// 保存上传设置
const saveUploadInfo = () => {
  // 模拟API保存数据
  console.log('保存上传设置:', uploadForm)
  ElMessage.success('上传设置保存成功')
}

// 保存商城设置
const saveShopInfo = () => {
  // 模拟API保存数据
  console.log('保存商城设置:', shopForm)
  ElMessage.success('商城设置保存成功')
}

// 测试上传
const testUpload = () => {
  ElMessage.info('请选择一个文件上传')
  // 实际应该打开一个文件选择器
}

onMounted(() => {
  // 获取各项设置
  getSiteInfo()
  getWechatInfo()
  getUploadInfo()
  getShopInfo()
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

.setting-form {
  max-width: 800px;
  margin-top: 20px;
}

.form-help {
  margin-left: 10px;
  color: #606266;
}

.avatar-uploader {
  :deep(.el-upload) {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: var(--el-transition-duration-fast);

    &:hover {
      border-color: var(--el-color-primary);
    }
  }
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  text-align: center;
  line-height: 100px;
}

.avatar {
  width: 100px;
  height: 100px;
  display: block;
}
</style> 