<template>
  <div class="app-container">
    <div class="page-header">
      <el-row :gutter="20" type="flex" justify="space-between" align="middle">
        <el-col :span="12">
          <h2 class="page-title">商品分类管理</h2>
        </el-col>
        <el-col :span="12" style="text-align: right">
          <el-button type="primary" @click="handleAdd">添加分类</el-button>
        </el-col>
      </el-row>
    </div>

    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>商品分类</span>
          <el-button type="primary" size="small" @click="handleAdd">添加分类</el-button>
        </div>
      </template>
      <div class="category-list">
        <el-table :data="tableData" style="width: 100%" row-key="id" border default-expand-all v-loading="loading">
          <el-table-column prop="name" label="分类名称">
            <template #default="scope">
              <span>{{ scope.row.name }}</span>
              <el-tag v-if="scope.row.icon" size="small" style="margin-left: 10px">
                <el-icon><Picture /></el-icon>
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="parent_id" label="父级分类" width="150">
            <template #default="scope">
              {{ getParentName(scope.row.parent_id) }}
            </template>
          </el-table-column>
          <el-table-column prop="sort_order" label="排序" width="120"></el-table-column>
          <el-table-column prop="is_visible" label="状态" width="120">
            <template #default="scope">
              <el-tag :type="scope.row.is_visible ? 'success' : 'danger'">
                {{ scope.row.is_visible ? '显示' : '隐藏' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200">
            <template #default="scope">
              <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 分类表单对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="父级分类">
          <el-select v-model="form.parent_id" placeholder="请选择父级分类" style="width: 100%">
            <el-option :value="0" label="一级分类"></el-option>
            <el-option
              v-for="item in parentCategories"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="分类名称">
          <el-input v-model="form.name" placeholder="请输入分类名称"></el-input>
        </el-form-item>
        <el-form-item label="分类图标">
          <el-upload
            class="avatar-uploader"
            action="/api/upload"
            :show-file-list="false"
            :on-success="handleIconSuccess"
            :before-upload="beforeIconUpload"
          >
            <img v-if="form.icon" :src="form.icon" class="avatar">
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="分类Banner">
          <el-upload
            class="avatar-uploader"
            action="/api/upload"
            :show-file-list="false"
            :on-success="handleBannerSuccess"
            :before-upload="beforeBannerUpload"
          >
            <img v-if="form.banner" :src="form.banner" class="avatar">
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.sort_order" :min="0" :step="1"></el-input-number>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="form.is_visible" :active-value="1" :inactive-value="0"></el-switch>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Picture, Plus } from '@element-plus/icons-vue'
import { getCategoryList, createCategory, updateCategory, deleteCategory } from '@/api/product'

const tableData = ref([])
const loading = ref(false)

const dialogVisible = ref(false)
const dialogTitle = ref('添加分类')
const form = ref({
  id: null,
  parent_id: 0,
  name: '',
  icon: '',
  banner: '',
  sort_order: 0,
  is_visible: 1
})

// 获取父级分类列表（排除当前编辑的分类）
const parentCategories = computed(() => {
  if (!form.value.id) return tableData.value
  return tableData.value.filter(item => item.id !== form.value.id)
})

// 根据父级ID获取父级分类名称
const getParentName = (parentId) => {
  if (parentId === 0) return '一级分类'
  const parent = tableData.value.find(item => item.id === parentId)
  return parent ? parent.name : '未知分类'
}

// 加载分类列表数据
const fetchCategoryList = async () => {
  loading.value = true
  try {
    console.log('[DEBUG] 开始获取分类列表')
    const response = await getCategoryList()
    console.log('[DEBUG] 获取分类列表响应:', response)
    if (!response || !response.data) {
      console.error('[ERROR] 获取分类列表响应数据格式错误:', response)
      throw new Error('响应数据格式错误')
    }
    tableData.value = response.data
    console.log('[DEBUG] 更新表格数据:', tableData.value)
  } catch (error) {
    console.error('[ERROR] 获取分类列表失败:', error)
    ElMessage.error('获取分类列表失败: ' + (error.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  dialogTitle.value = '添加分类'
  form.value = {
    id: null,
    parent_id: 0,
    name: '',
    icon: '',
    banner: '',
    sort_order: 0,
    is_visible: 1
  }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑分类'
  form.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm(`确定要删除分类 "${row.name}" 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      console.log('开始删除分类:', row.id)
      await deleteCategory(row.id)
      ElMessage.success('删除分类成功')
      fetchCategoryList() // 刷新列表
    } catch (error) {
      console.error('删除分类失败:', error)
      ElMessage.error('删除分类失败')
    }
  }).catch(() => {
    // 取消删除
  })
}

// 处理图标上传成功
const handleIconSuccess = (response) => {
  form.value.icon = response.data.url
  ElMessage.success('图标上传成功')
}

// 处理Banner上传成功
const handleBannerSuccess = (response) => {
  form.value.banner = response.data.url
  ElMessage.success('Banner上传成功')
}

// 上传前检查
const beforeIconUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB!')
    return false
  }
  return true
}

const beforeBannerUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt5M = file.size / 1024 / 1024 < 5

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt5M) {
    ElMessage.error('图片大小不能超过 5MB!')
    return false
  }
  return true
}

const handleSubmit = async () => {
  console.log('[DEBUG] 开始提交表单:', form.value)
  
  if (!form.value.name) {
    console.warn('[WARN] 分类名称为空')
    ElMessage.warning('请输入分类名称')
    return
  }
  
  try {
    if (form.value.id) {
      // 编辑分类
      console.log('[DEBUG] 开始更新分类:', form.value)
      const updateResponse = await updateCategory(form.value.id, form.value)
      console.log('[DEBUG] 更新分类响应:', updateResponse)
      ElMessage.success('更新分类成功')
    } else {
      // 添加分类
      console.log('[DEBUG] 开始创建分类:', form.value)
      const createResponse = await createCategory(form.value)
      console.log('[DEBUG] 创建分类响应:', createResponse)
      ElMessage.success('添加分类成功')
    }
    
    dialogVisible.value = false
    console.log('[DEBUG] 关闭对话框，准备刷新列表')
    
    // 立即刷新列表
    await fetchCategoryList()
    console.log('[DEBUG] 列表刷新完成')
    
  } catch (error) {
    console.error('[ERROR] 保存分类失败:', error)
    
    // 详细的错误信息处理
    let errorMsg = '未知错误'
    if (error.response) {
      console.error('[ERROR] 错误响应:', error.response)
      if (error.response.data) {
        console.error('[ERROR] 错误响应数据:', error.response.data)
        if (typeof error.response.data === 'string') {
          errorMsg = error.response.data
        } else if (error.response.data.message) {
          errorMsg = error.response.data.message
        } else if (error.response.data.error) {
          errorMsg = error.response.data.error
        }
      }
    } else if (error.request) {
      console.error('[ERROR] 请求错误:', error.request)
      errorMsg = '请求失败，请检查网络连接'
    } else {
      console.error('[ERROR] 其他错误:', error.message)
      errorMsg = error.message
    }
    
    ElMessage.error(`保存分类失败: ${errorMsg}`)
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchCategoryList()
})
</script>

<style lang="scss" scoped>
.page-header {
  margin-bottom: 20px;
  
  .page-title {
    margin: 0;
    font-size: 20px;
    font-weight: 500;
  }
}

.category-list {
  padding: 20px 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.avatar-uploader {
  :deep(.el-upload) {
    border: 1px dashed var(--el-border-color);
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
  width: 178px;
  height: 178px;
  text-align: center;
  line-height: 178px;
}

.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>