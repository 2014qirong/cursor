<template>
  <!-- 页面容器 -->
  <div class="app-container">
    <!-- 卡片组件 -->
    <el-card class="box-card">
      <!-- 卡片头部 -->
      <template #header>
        <div class="card-header">
          <span>编辑文章</span>
          <div>
            <el-button @click="cancel">取消</el-button>
            <el-button type="primary" @click="submitForm">保存</el-button>
          </div>
        </div>
      </template>
      
      <!-- 加载中 -->
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="10" animated />
      </div>
      
      <!-- 表单 -->
      <el-form v-else :model="articleForm" ref="articleFormRef" :rules="rules" label-width="100px">
        <el-form-item label="文章标题" prop="title">
          <el-input v-model="articleForm.title" placeholder="请输入文章标题" />
        </el-form-item>
        
        <el-form-item label="文章分类" prop="categoryId">
          <el-select v-model="articleForm.categoryId" placeholder="请选择文章分类" style="width: 100%">
            <el-option 
              v-for="item in categoryOptions" 
              :key="item.id" 
              :label="item.name" 
              :value="item.id" 
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="封面图片" prop="coverImage">
          <el-upload
            class="avatar-uploader"
            action="#"
            :show-file-list="false"
            :auto-upload="false"
            :on-change="handleImageChange"
          >
            <img v-if="articleForm.coverImage" :src="articleForm.coverImage" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
          <div class="image-tip">建议上传尺寸：750px * 400px，大小不超过2MB</div>
        </el-form-item>
        
        <el-form-item label="文章作者" prop="author">
          <el-input v-model="articleForm.author" placeholder="请输入作者" />
        </el-form-item>
        
        <el-form-item label="文章摘要" prop="summary">
          <el-input v-model="articleForm.summary" type="textarea" :rows="3" placeholder="请输入文章摘要" />
        </el-form-item>
        
        <el-form-item label="排序" prop="sort">
          <el-input-number v-model="articleForm.sort" :min="0" :max="9999" controls-position="right" />
        </el-form-item>
        
        <el-form-item label="置顶文章">
          <el-switch v-model="articleForm.isTop" :active-value="1" :inactive-value="0" />
        </el-form-item>
        
        <el-form-item label="状态">
          <el-radio-group v-model="articleForm.status">
            <el-radio :label="1">发布</el-radio>
            <el-radio :label="0">草稿</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="文章内容" prop="content">
          <div class="editor-container">
            <div class="editor-placeholder">富文本编辑器（此处为模拟，实际项目中可集成TinyMCE等编辑器）</div>
            <el-input type="textarea" v-model="articleForm.content" :rows="10" placeholder="请输入文章内容" />
          </div>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
// 引入组件和API
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter, useRoute } from 'vue-router'
import { Plus } from '@element-plus/icons-vue'

// 路由对象
const router = useRouter()
const route = useRoute()
const articleFormRef = ref(null)
const loading = ref(true)

// 文章表单数据
const articleForm = reactive({
  id: undefined,
  title: '',
  categoryId: undefined,
  coverImage: '',
  author: '',
  summary: '',
  content: '',
  sort: 0,
  isTop: 0,
  status: 1
})

// 表单验证规则
const rules = {
  title: [
    { required: true, message: '请输入文章标题', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  categoryId: [
    { required: true, message: '请选择文章分类', trigger: 'change' }
  ],
  author: [
    { required: true, message: '请输入作者', trigger: 'blur' }
  ],
  summary: [
    { required: true, message: '请输入文章摘要', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入文章内容', trigger: 'blur' }
  ]
}

// 文章分类选项
const categoryOptions = [
  { id: 1, name: '公司动态' },
  { id: 2, name: '行业资讯' },
  { id: 3, name: '产品教程' },
  { id: 4, name: '常见问题' }
]

// 获取文章详情
const getArticleDetail = (id) => {
  loading.value = true
  // 模拟API请求获取文章详情
  setTimeout(() => {
    // 模拟数据
    const article = {
      id: id,
      title: '2023年度电商行业发展趋势分析',
      categoryId: 2,
      coverImage: 'https://img.alicdn.com/imgextra/i4/O1CN01uqZUwv29MYhSN2Pc5_!!6000000008059-0-tps-1200-800.jpg',
      author: '张三',
      summary: '本文分析了2023年电商行业的发展趋势，包括社交电商的崛起、直播带货的常态化等现象。',
      content: '<p>随着互联网技术的不断发展，电子商务已经成为人们日常生活中不可或缺的一部分。2023年，电商行业呈现出以下几个明显的发展趋势：</p><p>1. <strong>社交电商的持续崛起</strong>：社交媒体与电商的深度融合，让购物体验更加社交化、互动化，消费者可以通过朋友推荐、达人分享等方式发现商品。</p><p>2. <strong>直播带货的常态化</strong>：直播电商已从新兴模式变为主流渠道，各大平台持续加码，头部主播带货能力持续增强。</p><p>3. <strong>下沉市场潜力释放</strong>：三四线城市及农村地区的消费潜力正在被逐步挖掘，成为电商平台争夺的新蓝海。</p>',
      sort: 1,
      isTop: 1,
      status: 1
    }
    
    // 更新表单数据
    Object.keys(article).forEach(key => {
      if (articleForm.hasOwnProperty(key)) {
        articleForm[key] = article[key]
      }
    })
    
    loading.value = false
  }, 1000)
}

// 图片上传处理
const handleImageChange = (file) => {
  // 模拟图片上传，实际项目中应调用上传接口
  const reader = new FileReader()
  reader.readAsDataURL(file.raw)
  reader.onload = () => {
    articleForm.coverImage = reader.result
  }
}

// 提交表单
const submitForm = () => {
  articleFormRef.value.validate((valid) => {
    if (valid) {
      // 模拟更新文章API调用
      setTimeout(() => {
        ElMessage.success('更新文章成功')
        router.push('/content/article')
      }, 500)
    } else {
      return false
    }
  })
}

// 取消
const cancel = () => {
  router.push('/content/article')
}

// 组件挂载时获取文章详情
onMounted(() => {
  const id = route.params.id
  if (id) {
    getArticleDetail(parseInt(id))
  } else {
    loading.value = false
  }
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.loading-container {
  padding: 20px;
}
.avatar-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 200px;
}
.avatar-uploader:hover {
  border-color: #409eff;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 200px;
  height: 120px;
  line-height: 120px;
  text-align: center;
}
.avatar {
  width: 200px;
  height: 120px;
  display: block;
  object-fit: cover;
}
.image-tip {
  font-size: 12px;
  color: #909399;
  line-height: 1.5;
  margin-top: 5px;
}
.editor-container {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}
.editor-placeholder {
  background-color: #f5f7fa;
  text-align: center;
  padding: 10px;
  color: #909399;
  font-size: 14px;
}
</style> 