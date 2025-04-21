<template>
  <div class="notice-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>公告管理</span>
          <el-button type="primary" @click="handleAdd">新增公告</el-button>
        </div>
      </template>
      
      <!-- 搜索表单 -->
      <el-form :inline="true" :model="queryParams" class="search-form">
        <el-form-item label="公告标题">
          <el-input v-model="queryParams.title" placeholder="请输入公告标题" clearable @keyup.enter="handleQuery" />
        </el-form-item>
        <el-form-item label="公告类型">
          <el-select v-model="queryParams.type" placeholder="请选择公告类型" clearable>
            <el-option v-for="item in typeOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="queryParams.status" placeholder="请选择状态" clearable>
            <el-option label="已发布" :value="1" />
            <el-option label="未发布" :value="0" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery">查询</el-button>
          <el-button @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 表格 -->
      <el-table
        v-loading="loading"
        :data="noticeList"
        style="width: 100%"
        border
      >
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="title" label="公告标题" min-width="200" show-overflow-tooltip />
        <el-table-column prop="type" label="公告类型" width="120" align="center">
          <template #default="scope">
            <el-tag :type="getNoticeTypeTag(scope.row.type)">
              {{ getNoticeTypeText(scope.row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="publishTime" label="发布时间" width="160" show-overflow-tooltip />
        <el-table-column prop="sort" label="排序" width="80" align="center" />
        <el-table-column prop="isTop" label="是否置顶" width="100" align="center">
          <template #default="scope">
            <el-switch
              v-model="scope.row.isTop"
              :active-value="1"
              :inactive-value="0"
              @change="handleTopChange(scope.row)"
            />
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.status === 1 ? 'success' : 'info'">
              {{ scope.row.status === 1 ? '已发布' : '未发布' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" align="center" fixed="right">
          <template #default="scope">
            <el-button link type="primary" @click="handleView(scope.row)">查看</el-button>
            <el-button link type="primary" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button 
              link 
              :type="scope.row.status === 0 ? 'success' : 'warning'" 
              @click="handleStatusChange(scope.row)"
            >
              {{ scope.row.status === 0 ? '发布' : '撤回' }}
            </el-button>
            <el-button link type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="queryParams.pageNum"
          v-model:page-size="queryParams.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 添加/编辑公告对话框 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="700px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="noticeFormRef"
        :model="noticeForm"
        :rules="noticeRules"
        label-width="100px"
      >
        <el-form-item label="公告标题" prop="title">
          <el-input v-model="noticeForm.title" placeholder="请输入公告标题" />
        </el-form-item>
        <el-form-item label="公告类型" prop="type">
          <el-select v-model="noticeForm.type" placeholder="请选择公告类型" style="width: 100%">
            <el-option v-for="item in typeOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="公告内容" prop="content">
          <el-input
            v-model="noticeForm.content"
            type="textarea"
            :rows="10"
            placeholder="请输入公告内容"
          />
        </el-form-item>
        <el-form-item label="排序" prop="sort">
          <el-input-number v-model="noticeForm.sort" :min="0" :max="9999" controls-position="right" style="width: 100%" />
        </el-form-item>
        <el-form-item label="是否置顶" prop="isTop">
          <el-switch
            v-model="noticeForm.isTop"
            :active-value="1"
            :inactive-value="0"
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="noticeForm.status">
            <el-radio :label="1">发布</el-radio>
            <el-radio :label="0">草稿</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitForm">确 定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 公告查看对话框 -->
    <el-dialog
      title="公告详情"
      v-model="viewDialogVisible"
      width="700px"
    >
      <div class="notice-view">
        <div class="notice-title">{{ noticeDetail.title }}</div>
        <div class="notice-info">
          <span>类型：{{ getNoticeTypeText(noticeDetail.type) }}</span>
          <span>发布时间：{{ noticeDetail.publishTime }}</span>
        </div>
        <div class="notice-content">{{ noticeDetail.content }}</div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getNoticeList, addNotice, updateNotice, deleteNotice } from '@/api/content'

// 查询参数
const queryParams = reactive({
  pageNum: 1,
  pageSize: 10,
  title: '',
  type: '',
  status: ''
})

// 公告类型选项
const typeOptions = [
  { value: 1, label: '系统公告' },
  { value: 2, label: '活动公告' },
  { value: 3, label: '商品公告' },
  { value: 4, label: '其他公告' }
]

// 公告列表数据
const loading = ref(false)
const noticeList = ref([])
const total = ref(0)

// 表单对话框
const dialogVisible = ref(false)
const dialogTitle = ref('添加公告')
const noticeFormRef = ref(null)
const noticeForm = reactive({
  id: '',
  title: '',
  type: 1,
  content: '',
  sort: 0,
  isTop: 0,
  status: 0
})

// 查看对话框
const viewDialogVisible = ref(false)
const noticeDetail = reactive({
  id: '',
  title: '',
  type: 1,
  content: '',
  publishTime: '',
  sort: 0,
  isTop: 0,
  status: 0
})

// 表单校验规则
const noticeRules = {
  title: [
    { required: true, message: '请输入公告标题', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择公告类型', trigger: 'change' }
  ],
  content: [
    { required: true, message: '请输入公告内容', trigger: 'blur' }
  ]
}

// 获取公告列表
const getList = async () => {
  loading.value = true
  try {
    const res = await getNoticeList(queryParams)
    noticeList.value = res.data.list || []
    total.value = res.data.total || 0
  } catch (error) {
    console.error('获取公告列表失败', error)
  } finally {
    loading.value = false
  }
}

// 获取公告类型文本
const getNoticeTypeText = (type) => {
  const found = typeOptions.find(item => item.value === type)
  return found ? found.label : '未知类型'
}

// 获取公告类型标签样式
const getNoticeTypeTag = (type) => {
  const typeMap = {
    1: 'primary',
    2: 'success',
    3: 'warning',
    4: 'info'
  }
  return typeMap[type] || 'info'
}

// 查询操作
const handleQuery = () => {
  queryParams.pageNum = 1
  getList()
}

// 重置查询条件
const resetQuery = () => {
  Object.assign(queryParams, {
    pageNum: 1,
    pageSize: 10,
    title: '',
    type: '',
    status: ''
  })
  getList()
}

// 分页大小改变
const handleSizeChange = (size) => {
  queryParams.pageSize = size
  getList()
}

// 分页页码改变
const handleCurrentChange = (current) => {
  queryParams.pageNum = current
  getList()
}

// 新增公告
const handleAdd = () => {
  resetForm()
  dialogTitle.value = '添加公告'
  dialogVisible.value = true
}

// 查看公告
const handleView = (row) => {
  Object.assign(noticeDetail, row)
  viewDialogVisible.value = true
}

// 编辑公告
const handleEdit = (row) => {
  resetForm()
  dialogTitle.value = '编辑公告'
  
  // 填充表单数据
  Object.assign(noticeForm, {
    id: row.id,
    title: row.title,
    type: row.type,
    content: row.content,
    sort: row.sort,
    isTop: row.isTop,
    status: row.status
  })
  
  dialogVisible.value = true
}

// 改变公告状态
const handleStatusChange = async (row) => {
  const text = row.status === 0 ? '发布' : '撤回'
  const newStatus = row.status === 0 ? 1 : 0
  
  ElMessageBox.confirm(
    `确认要${text}该公告吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await updateNotice(row.id, { status: newStatus })
      ElMessage.success(`${text}成功`)
      // 修改本地数据
      row.status = newStatus
      
      // 更新发布时间
      if (newStatus === 1) {
        row.publishTime = new Date().toLocaleString()
      }
    } catch (error) {
      console.error(`${text}失败`, error)
      ElMessage.error(`${text}失败`)
    }
  }).catch(() => {})
}

// 改变置顶状态
const handleTopChange = async (row) => {
  try {
    await updateNotice(row.id, { isTop: row.isTop })
    ElMessage.success(row.isTop === 1 ? '置顶成功' : '取消置顶成功')
  } catch (error) {
    console.error('更新置顶状态失败', error)
    ElMessage.error('操作失败')
    // 恢复原值
    row.isTop = row.isTop === 1 ? 0 : 1
  }
}

// 删除公告
const handleDelete = (row) => {
  ElMessageBox.confirm(
    '确认要删除该公告吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteNotice(row.id)
      ElMessage.success('删除成功')
      // 刷新列表
      getList()
    } catch (error) {
      console.error('删除失败', error)
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

// 提交表单
const submitForm = async () => {
  if (!noticeFormRef.value) return
  
  await noticeFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (noticeForm.id) {
          // 更新
          await updateNotice(noticeForm.id, noticeForm)
          ElMessage.success('更新成功')
        } else {
          // 添加
          await addNotice(noticeForm)
          ElMessage.success('添加成功')
        }
        
        dialogVisible.value = false
        getList()
      } catch (error) {
        console.error('保存失败', error)
        ElMessage.error('保存失败')
      }
    }
  })
}

// 重置表单
const resetForm = () => {
  if (noticeFormRef.value) {
    noticeFormRef.value.resetFields()
  }
  
  Object.assign(noticeForm, {
    id: '',
    title: '',
    type: 1,
    content: '',
    sort: 0,
    isTop: 0,
    status: 0
  })
}

onMounted(() => {
  getList()
})
</script>

<style lang="scss" scoped>
.notice-container {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .search-form {
    margin-bottom: 20px;
  }
  
  .pagination-container {
    margin-top: 20px;
    text-align: right;
  }
  
  .notice-view {
    .notice-title {
      font-size: 18px;
      font-weight: bold;
      text-align: center;
      margin-bottom: 15px;
    }
    
    .notice-info {
      display: flex;
      justify-content: space-between;
      color: #909399;
      font-size: 13px;
      padding: 10px 0;
      border-bottom: 1px solid #ebeef5;
      margin-bottom: 15px;
    }
    
    .notice-content {
      padding: 10px;
      line-height: 1.6;
      min-height: 200px;
      white-space: pre-wrap;
    }
  }
}
</style> 