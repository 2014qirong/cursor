<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>文章管理</span>
          <el-button type="primary" @click="handleAddArticle">新增文章</el-button>
        </div>
      </template>

      <el-table
        v-loading="loading"
        :data="articleList"
        border
        style="width: 100%"
      >
        <el-table-column type="index" label="序号" width="50" />
        <el-table-column prop="title" label="文章标题" min-width="120" show-overflow-tooltip />
        <el-table-column label="封面图片" width="120">
          <template #default="scope">
            <el-image
              style="width: 80px; height: 60px"
              :src="scope.row.coverImage"
              fit="cover"
              :preview-src-list="[scope.row.coverImage]"
            />
          </template>
        </el-table-column>
        <el-table-column prop="categoryName" label="文章分类" width="100" />
        <el-table-column prop="author" label="作者" width="100" />
        <el-table-column prop="viewCount" label="浏览量" width="80" align="center" />
        <el-table-column prop="sort" label="排序" width="70" align="center" />
        <el-table-column prop="isTop" label="是否置顶" width="80" align="center">
          <template #default="scope">
            <el-tag v-if="scope.row.isTop === 1" type="success">是</el-tag>
            <el-tag v-else type="info">否</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="80" align="center">
          <template #default="scope">
            <el-switch
              v-model="scope.row.status"
              :active-value="1"
              :inactive-value="0"
              @change="handleStatusChange(scope.row)"
            />
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="160" />
        <el-table-column label="操作" width="180" fixed="right">
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
              @click="handlePreview(scope.row)"
            >
              预览
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
      
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="queryParams.page"
          v-model:page-size="queryParams.limit"
          :total="total"
          :page-sizes="[10, 20, 30, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 添加/编辑文章对话框 -->
    <el-dialog
      :title="dialogType === 'add' ? '新增文章' : '编辑文章'"
      v-model="dialogVisible"
      width="800px"
    >
      <el-form
        ref="articleFormRef"
        :model="articleForm"
        :rules="articleRules"
        label-width="100px"
      >
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
            class="article-uploader"
            action="#"
            :auto-upload="false"
            :show-file-list="false"
            :on-change="handleImageChange"
          >
            <img v-if="articleForm.coverImage" :src="articleForm.coverImage" class="preview-img" />
            <el-icon v-else class="article-uploader-icon"><Plus /></el-icon>
          </el-upload>
          <div class="upload-tip">建议上传16:9比例的图片，最佳尺寸800x450像素</div>
        </el-form-item>
        <el-form-item label="作者" prop="author">
          <el-input v-model="articleForm.author" placeholder="请输入作者名称" />
        </el-form-item>
        <el-form-item label="文章摘要" prop="summary">
          <el-input 
            v-model="articleForm.summary" 
            type="textarea" 
            :rows="3"
            placeholder="请输入文章摘要" 
            maxlength="200"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="文章内容" prop="content">
          <div class="editor-container">
            <!-- 实际项目中应引入富文本编辑器组件 -->
            <el-input 
              v-model="articleForm.content" 
              type="textarea" 
              :rows="8"
              placeholder="请输入文章内容" 
            />
          </div>
        </el-form-item>
        <el-form-item label="排序" prop="sort">
          <el-input-number v-model="articleForm.sort" :min="0" :max="999" />
        </el-form-item>
        <el-form-item label="是否置顶">
          <el-radio-group v-model="articleForm.isTop">
            <el-radio :label="1">是</el-radio>
            <el-radio :label="0">否</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="articleForm.status">
            <el-radio :label="1">发布</el-radio>
            <el-radio :label="0">草稿</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 文章预览对话框 -->
    <el-dialog
      title="文章预览"
      v-model="previewVisible"
      width="800px"
      class="preview-dialog"
    >
      <div class="article-preview">
        <h1 class="article-title">{{ previewArticle.title }}</h1>
        <div class="article-meta">
          <span>作者：{{ previewArticle.author }}</span>
          <span>分类：{{ previewArticle.categoryName }}</span>
          <span>发布时间：{{ previewArticle.createTime }}</span>
          <span>浏览量：{{ previewArticle.viewCount }}</span>
        </div>
        <div v-if="previewArticle.coverImage" class="article-cover">
          <img :src="previewArticle.coverImage" alt="文章封面" />
        </div>
        <div class="article-summary">
          <strong>摘要：</strong>{{ previewArticle.summary }}
        </div>
        <div class="article-content" v-html="previewArticle.content"></div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

// 页面加载状态
const loading = ref(false)

// 文章分类选项
const categoryOptions = ref([
  { id: 1, name: '公司动态' },
  { id: 2, name: '行业资讯' },
  { id: 3, name: '产品教程' },
  { id: 4, name: '常见问题' }
])

// 文章列表数据
const articleList = ref([
  {
    id: 1,
    title: '2023年度电商行业发展趋势分析',
    coverImage: 'https://img.alicdn.com/imgextra/i4/O1CN01uqZUwv29MYhSN2Pc5_!!6000000008059-0-tps-1200-800.jpg',
    categoryId: 2,
    categoryName: '行业资讯',
    author: '张三',
    viewCount: 1256,
    summary: '本文分析了2023年电商行业的发展趋势，包括社交电商的崛起、直播带货的常态化等现象。',
    content: '<p>随着互联网技术的不断发展，电子商务已经成为人们日常生活中不可或缺的一部分...</p>',
    sort: 1,
    isTop: 1,
    status: 1,
    createTime: '2023-04-15 10:12:36'
  },
  {
    id: 2,
    title: '如何使用我们的会员积分系统',
    coverImage: 'https://img.alicdn.com/imgextra/i2/O1CN01HoRQZ21o7xN5DIoL0_!!6000000005177-0-tps-1200-800.jpg',
    categoryId: 3,
    categoryName: '产品教程',
    author: '李四',
    viewCount: 856,
    summary: '详细介绍了会员积分系统的使用方法，包括积分获取、兑换和查询等操作指南。',
    content: '<p>会员积分是回馈用户的重要方式，通过本教程，您将了解如何高效地使用我们的积分系统...</p>',
    sort: 2,
    isTop: 0,
    status: 1,
    createTime: '2023-04-20 14:25:18'
  },
  {
    id: 3,
    title: '关于平台售后服务政策调整的公告',
    coverImage: 'https://img.alicdn.com/imgextra/i3/O1CN01FgRJHQ1rEOZDw2wen_!!6000000005597-0-tps-1200-800.jpg',
    categoryId: 1,
    categoryName: '公司动态',
    author: '王五',
    viewCount: 2103,
    summary: '本公告宣布了平台售后服务政策的最新调整，旨在提升用户体验和服务质量。',
    content: '<p>为了进一步提升用户购物体验，我们对售后服务政策进行了全面升级...</p>',
    sort: 3,
    isTop: 1,
    status: 1,
    createTime: '2023-04-22 09:36:42'
  }
])

// 查询参数
const queryParams = reactive({
  page: 1,
  limit: 10,
  title: '',
  categoryId: null,
  status: null
})

// 总条数
const total = ref(3)

// 文章表单相关
const dialogVisible = ref(false)
const dialogType = ref('add')
const articleFormRef = ref(null)
const articleForm = reactive({
  id: undefined,
  title: '',
  coverImage: '',
  categoryId: null,
  author: '',
  summary: '',
  content: '',
  sort: 0,
  isTop: 0,
  status: 1
})

// 表单验证规则
const articleRules = {
  title: [
    { required: true, message: '请输入文章标题', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  categoryId: [
    { required: true, message: '请选择文章分类', trigger: 'change' }
  ],
  coverImage: [
    { required: true, message: '请上传文章封面图片', trigger: 'change' }
  ],
  author: [
    { required: true, message: '请输入作者名称', trigger: 'blur' }
  ],
  summary: [
    { required: true, message: '请输入文章摘要', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入文章内容', trigger: 'blur' }
  ]
}

// 预览相关
const previewVisible = ref(false)
const previewArticle = ref({})

// 处理页码变化
const handleCurrentChange = (val) => {
  queryParams.page = val
  getArticleList()
}

// 处理每页条数变化
const handleSizeChange = (val) => {
  queryParams.limit = val
  getArticleList()
}

// 获取文章列表
const getArticleList = () => {
  loading.value = true
  // 这里应该调用API获取文章列表
  setTimeout(() => {
    loading.value = false
  }, 500)
}

// 处理添加文章
const handleAddArticle = () => {
  resetForm()
  dialogType.value = 'add'
  dialogVisible.value = true
}

// 处理编辑文章
const handleEdit = (row) => {
  resetForm()
  dialogType.value = 'edit'
  Object.assign(articleForm, { ...row })
  dialogVisible.value = true
}

// 处理预览文章
const handlePreview = (row) => {
  previewArticle.value = { ...row }
  previewVisible.value = true
}

// 重置表单
const resetForm = () => {
  if (articleFormRef.value) {
    articleFormRef.value.resetFields()
  }
  Object.assign(articleForm, {
    id: undefined,
    title: '',
    coverImage: '',
    categoryId: null,
    author: '',
    summary: '',
    content: '',
    sort: 0,
    isTop: 0,
    status: 1
  })
}

// 处理封面图片上传
const handleImageChange = (file) => {
  // 实际项目中应上传到服务器获取URL
  // 这里仅做演示，直接使用本地预览
  const reader = new FileReader()
  reader.onload = (e) => {
    articleForm.coverImage = e.target.result
  }
  reader.readAsDataURL(file.raw)
}

// 提交表单
const submitForm = () => {
  if (!articleFormRef.value) return
  
  articleFormRef.value.validate((valid) => {
    if (valid) {
      if (dialogType.value === 'add') {
        // 新增文章
        const newArticle = { ...articleForm }
        newArticle.id = Date.now()
        newArticle.createTime = new Date().toLocaleString()
        newArticle.viewCount = 0
        // 根据分类ID获取分类名称
        const category = categoryOptions.value.find(item => item.id === newArticle.categoryId)
        newArticle.categoryName = category ? category.name : ''
        articleList.value.push(newArticle)
        ElMessage.success('新增文章成功')
      } else {
        // 编辑文章
        const index = articleList.value.findIndex(item => item.id === articleForm.id)
        if (index !== -1) {
          // 更新分类名称
          const category = categoryOptions.value.find(item => item.id === articleForm.categoryId)
          articleForm.categoryName = category ? category.name : ''
          articleList.value[index] = { ...articleList.value[index], ...articleForm }
          ElMessage.success('修改文章成功')
        }
      }
      dialogVisible.value = false
    }
  })
}

// 处理删除文章
const handleDelete = (row) => {
  ElMessageBox.confirm(`确认删除文章 "${row.title}" ?`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 实际应调用API删除
    const index = articleList.value.findIndex(item => item.id === row.id)
    if (index !== -1) {
      articleList.value.splice(index, 1)
      ElMessage.success('删除成功')
    }
  }).catch(() => {})
}

// 处理状态变更
const handleStatusChange = (row) => {
  const text = row.status === 1 ? '发布' : '设为草稿'
  ElMessage.success(`已将文章"${row.title}"${text}`)
}

onMounted(() => {
  getArticleList()
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

.pagination-container {
  margin-top: 15px;
  display: flex;
  justify-content: center;
}

.article-uploader {
  .preview-img {
    width: 200px;
    height: 112px;
    display: block;
    object-fit: cover;
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
  }
  
  .article-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 200px;
    height: 112px;
    line-height: 112px;
    text-align: center;
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
  }
}

.upload-tip {
  font-size: 12px;
  color: #606266;
  margin-top: 5px;
}

.editor-container {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

.article-preview {
  padding: 0 15px;
  
  .article-title {
    font-size: 24px;
    text-align: center;
    margin-bottom: 15px;
  }
  
  .article-meta {
    display: flex;
    flex-wrap: wrap;
    font-size: 13px;
    color: #909399;
    margin-bottom: 20px;
    justify-content: center;
    
    span {
      margin-right: 15px;
    }
  }
  
  .article-cover {
    margin-bottom: 20px;
    text-align: center;
    
    img {
      max-width: 100%;
      max-height: 400px;
      border-radius: 4px;
    }
  }
  
  .article-summary {
    background-color: #f7f7f7;
    padding: 12px 15px;
    border-radius: 4px;
    margin-bottom: 20px;
    font-size: 14px;
    line-height: 1.6;
    color: #606266;
  }
  
  .article-content {
    line-height: 1.8;
    font-size: 15px;
    color: #333;
  }
}
</style> 