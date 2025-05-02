<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>轮播图管理</span>
          <el-button type="primary" @click="handleAddBanner">新增轮播图</el-button>
        </div>
      </template>

      <el-table
        v-loading="loading"
        :data="bannerList"
        border
        style="width: 100%"
      >
        <el-table-column type="index" label="序号" width="50" />
        <el-table-column prop="title" label="轮播标题" min-width="100" />
        <el-table-column label="轮播图片" width="200">
          <template #default="scope">
            <el-image
              style="width: 150px; height: 60px"
              :src="scope.row.imgUrl"
              fit="contain"
              :preview-src-list="[scope.row.imgUrl]"
            />
          </template>
        </el-table-column>
        <el-table-column prop="type" label="轮播类型" width="120">
          <template #default="scope">
            <el-tag v-if="scope.row.type === 1">商品</el-tag>
            <el-tag v-else-if="scope.row.type === 2" type="success">专题</el-tag>
            <el-tag v-else-if="scope.row.type === 3" type="warning">外部链接</el-tag>
            <el-tag v-else type="info">其他</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="url" label="链接地址" min-width="180" />
        <el-table-column prop="sort" label="排序" width="80" align="center" />
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
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column label="操作" width="150" fixed="right">
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

    <!-- 添加/编辑轮播图对话框 -->
    <el-dialog
      :title="dialogType === 'add' ? '新增轮播图' : '编辑轮播图'"
      v-model="dialogVisible"
      width="600px"
    >
      <el-form
        ref="bannerFormRef"
        :model="bannerForm"
        :rules="bannerRules"
        label-width="100px"
      >
        <el-form-item label="轮播标题" prop="title">
          <el-input v-model="bannerForm.title" placeholder="请输入轮播图标题" />
        </el-form-item>
        <el-form-item label="轮播图片" prop="imgUrl">
          <el-upload
            class="banner-uploader"
            action="#"
            :auto-upload="false"
            :show-file-list="false"
            :on-change="handleImageChange"
          >
            <img v-if="bannerForm.imgUrl" :src="bannerForm.imgUrl" class="preview-img" />
            <el-icon v-else class="banner-uploader-icon"><Plus /></el-icon>
          </el-upload>
          <div class="upload-tip">建议上传尺寸为1200x400像素的图片</div>
        </el-form-item>
        <el-form-item label="轮播类型" prop="type">
          <el-select v-model="bannerForm.type" placeholder="请选择轮播类型" style="width: 100%">
            <el-option label="商品" :value="1" />
            <el-option label="专题" :value="2" />
            <el-option label="外部链接" :value="3" />
            <el-option label="其他" :value="4" />
          </el-select>
        </el-form-item>
        <el-form-item label="链接地址" prop="url">
          <el-input v-model="bannerForm.url" placeholder="请输入链接地址" />
        </el-form-item>
        <el-form-item label="排序" prop="sort">
          <el-input-number v-model="bannerForm.sort" :min="0" :max="999" />
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="bannerForm.status">
            <el-radio :label="1">启用</el-radio>
            <el-radio :label="0">禁用</el-radio>
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
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

// 页面加载状态
const loading = ref(false)

// 轮播图列表数据
const bannerList = ref([
  {
    id: 1,
    title: '新款春季上新',
    imgUrl: 'https://img.alicdn.com/imgextra/i1/O1CN01b5kcx91W9jOFbQ0Kn_!!6000000002744-2-tps-1125-352.png',
    type: 1,
    url: '/product/123',
    sort: 1,
    status: 1,
    createTime: '2023-03-15 10:12:36'
  },
  {
    id: 2,
    title: '618年中大促',
    imgUrl: 'https://img.alicdn.com/imgextra/i2/O1CN010ThlMq1jaUNV9SU5B_!!6000000004576-0-tps-1920-600.jpg',
    type: 2,
    url: '/topic/618',
    sort: 2,
    status: 1,
    createTime: '2023-03-20 14:25:18'
  },
  {
    id: 3,
    title: '品牌专场',
    imgUrl: 'https://img.alicdn.com/imgextra/i1/O1CN01MRVFUV1FGWvCBgn8i_!!6000000000463-2-tps-1125-352.png',
    type: 3,
    url: 'https://www.example.com/brand',
    sort: 3,
    status: 0,
    createTime: '2023-03-22 09:36:42'
  }
])

// 查询参数
const queryParams = reactive({
  page: 1,
  limit: 10,
  title: '',
  type: null,
  status: null
})

// 总条数
const total = ref(3)

// 轮播图表单相关
const dialogVisible = ref(false)
const dialogType = ref('add')
const bannerFormRef = ref(null)
const bannerForm = reactive({
  id: undefined,
  title: '',
  imgUrl: '',
  type: 1,
  url: '',
  sort: 0,
  status: 1
})

// 表单验证规则
const bannerRules = {
  title: [
    { required: true, message: '请输入轮播图标题', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  imgUrl: [
    { required: false, message: '请上传轮播图片或填写链接地址', trigger: 'change' }
  ],
  type: [
    { required: true, message: '请选择轮播类型', trigger: 'change' }
  ],
  url: [
    { required: false, message: '请输入链接地址或上传轮播图片', trigger: 'blur' }
  ]
}

// 处理页码变化
const handleCurrentChange = (val) => {
  queryParams.page = val
  getBannerList()
}

// 处理每页条数变化
const handleSizeChange = (val) => {
  queryParams.limit = val
  getBannerList()
}

// 获取轮播图列表
const getBannerList = () => {
  loading.value = true
  // 这里应该调用API获取轮播图列表
  setTimeout(() => {
    loading.value = false
  }, 500)
}

// 处理添加轮播图
const handleAddBanner = () => {
  resetForm()
  dialogType.value = 'add'
  dialogVisible.value = true
}

// 处理编辑轮播图
const handleEdit = (row) => {
  resetForm()
  dialogType.value = 'edit'
  Object.assign(bannerForm, { ...row })
  dialogVisible.value = true
}

// 重置表单
const resetForm = () => {
  if (bannerFormRef.value) {
    bannerFormRef.value.resetFields()
  }
  Object.assign(bannerForm, {
    id: undefined,
    title: '',
    imgUrl: '',
    type: 1,
    url: '',
    sort: 0,
    status: 1
  })
}

// 处理图片上传
const handleImageChange = (file) => {
  // 实际项目中应上传到服务器获取URL
  // 这里仅做演示，直接使用本地预览
  const reader = new FileReader()
  reader.onload = (e) => {
    bannerForm.imgUrl = e.target.result
  }
  reader.readAsDataURL(file.raw)
}

// 提交表单
const submitForm = () => {
  if (!bannerFormRef.value) return
  
  // 自定义验证：确保至少填写了图片或链接地址
  if (!bannerForm.imgUrl && !bannerForm.url) {
    ElMessage.error('请上传轮播图片或填写链接地址')
    return
  }
  
  bannerFormRef.value.validate((valid) => {
    if (valid) {
      if (dialogType.value === 'add') {
        // 新增轮播图
        const newBanner = { ...bannerForm }
        newBanner.id = Date.now()
        newBanner.createTime = new Date().toLocaleString()
        bannerList.value.push(newBanner)
        ElMessage.success('新增轮播图成功')
      } else {
        // 编辑轮播图
        const index = bannerList.value.findIndex(item => item.id === bannerForm.id)
        if (index !== -1) {
          bannerList.value[index] = { ...bannerList.value[index], ...bannerForm }
          ElMessage.success('修改轮播图成功')
        }
      }
      dialogVisible.value = false
    }
  })
}

// 处理删除轮播图
const handleDelete = (row) => {
  ElMessageBox.confirm(`确认删除轮播图 ${row.title} ?`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 实际应调用API删除
    const index = bannerList.value.findIndex(item => item.id === row.id)
    if (index !== -1) {
      bannerList.value.splice(index, 1)
      ElMessage.success('删除成功')
    }
  }).catch(() => {})
}

// 处理状态变更
const handleStatusChange = (row) => {
  const text = row.status === 1 ? '启用' : '禁用'
  ElMessage.success(`已${text}轮播图：${row.title}`)
}

onMounted(() => {
  getBannerList()
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

.banner-uploader {
  .preview-img {
    width: 300px;
    height: 100px;
    display: block;
    object-fit: contain;
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
  }
  
  .banner-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 300px;
    height: 100px;
    line-height: 100px;
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
</style> 