<template>
  <div class="app-container">
    <div class="page-header">
      <el-row :gutter="20" type="flex" justify="space-between" align="middle">
        <el-col :span="12">
          <h2 class="page-title">商品列表</h2>
        </el-col>
        <el-col :span="12" style="text-align: right">
          <el-button type="primary" @click="handleAdd">添加商品</el-button>
          <el-button type="primary" plain @click="handleBatchOperation">批量操作</el-button>
          <el-button type="success" plain @click="handleImportExport">导入/导出</el-button>
        </el-col>
      </el-row>
    </div>

    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>商品列表</span>
          <el-button type="primary" size="small" @click="$router.push('/product/add')">添加商品</el-button>
        </div>
      </template>
      
      <div class="filter-container">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="商品名称">
            <el-input v-model="searchForm.name" placeholder="请输入商品名称" clearable>
            </el-input>
          </el-form-item>
          <el-form-item label="商品分类">
            <el-select v-model="searchForm.category" placeholder="请选择分类" clearable>
              <el-option label="家电" value="appliance"></el-option>
              <el-option label="服装" value="clothing"></el-option>
              <el-option label="食品" value="food"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <el-table :data="tableData" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="商品名称" min-width="200"></el-table-column>
        <el-table-column prop="category" label="商品分类" width="120"></el-table-column>
        <el-table-column prop="price" label="价格" width="120">
          <template #default="scope">
            ¥{{ scope.row.price.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="stock" label="库存" width="100"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status ? 'success' : 'info'">
              {{ scope.row.status ? '上架' : '下架' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button 
              size="small" 
              :type="scope.row.status ? 'warning' : 'success'"
              @click="handleToggleStatus(scope.row)"
            >
              {{ scope.row.status ? '下架' : '上架' }}
            </el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          background
          layout="total, sizes, prev, pager, next, jumper"
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        >
        </el-pagination>
      </div>
    </el-card>

    <!-- 批量操作对话框 -->
    <el-dialog
      title="批量操作"
      v-model="batchDialogVisible"
      width="400px"
    >
      <el-form label-width="80px">
        <el-form-item label="操作类型">
          <el-select v-model="batchForm.operation" placeholder="请选择操作类型" style="width: 100%">
            <el-option label="批量上架" value="上架" />
            <el-option label="批量下架" value="下架" />
            <el-option label="设置标签" value="标签" />
            <el-option label="修改分类" value="分类" />
            <el-option label="批量删除" value="删除" />
          </el-select>
        </el-form-item>

        <el-form-item label="设置标签" v-if="batchForm.operation === '标签'">
          <el-checkbox-group v-model="batchForm.tags">
            <el-checkbox label="hot">热门</el-checkbox>
            <el-checkbox label="new">新品</el-checkbox>
            <el-checkbox label="recommend">推荐</el-checkbox>
          </el-checkbox-group>
        </el-form-item>

        <el-form-item label="选择分类" v-if="batchForm.operation === '分类'">
          <el-cascader
            v-model="batchForm.categoryId"
            :options="categoryOptions"
            placeholder="请选择商品分类"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="batchDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleBatchConfirm" :loading="batchLoading">确 定</el-button>
      </template>
    </el-dialog>

    <!-- 导入导出对话框 -->
    <el-dialog
      title="导入/导出"
      v-model="importExportDialogVisible"
      width="400px"
    >
      <div class="import-export-dialog">
        <el-tabs v-model="importExportTab">
          <el-tab-pane label="导入" name="import">
            <p>请选择Excel文件进行导入</p>
            <el-upload
              class="upload-demo"
              drag
              action="#"
              :auto-upload="false"
              :on-change="handleFileChange"
            >
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                将文件拖到此处，或<em>点击上传</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  只能上传 .xlsx, .xls 文件
                </div>
              </template>
            </el-upload>
            <div style="margin-top: 20px">
              <el-button type="primary" @click="handleDownloadTemplate">下载导入模板</el-button>
              <el-button type="success" @click="handleImport" :loading="importLoading">开始导入</el-button>
            </div>
          </el-tab-pane>
          <el-tab-pane label="导出" name="export">
            <p>选择导出内容</p>
            <el-radio-group v-model="exportForm.type">
              <el-radio label="all">全部商品</el-radio>
              <el-radio label="selected">选中商品</el-radio>
              <el-radio label="filtered">当前筛选结果</el-radio>
            </el-radio-group>
            <div style="margin-top: 20px">
              <el-button type="primary" @click="handleExport" :loading="exportLoading">开始导出</el-button>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()

// 加载状态
const loading = ref(false)
const batchLoading = ref(false)
const importLoading = ref(false)
const exportLoading = ref(false)

// 搜索表单
const searchForm = reactive({
  name: '',
  category: ''
})

// 分页信息
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 100
})

// 表格数据
const tableData = ref([
  {
    id: 1,
    name: '智能电视 55英寸',
    category: '家电',
    price: 3999.00,
    stock: 100,
    status: true
  },
  {
    id: 2,
    name: '男士休闲裤',
    category: '服装',
    price: 199.00,
    stock: 300,
    status: true
  },
  {
    id: 3,
    name: '巧克力蛋糕',
    category: '食品',
    price: 88.00,
    stock: 50,
    status: false
  },
  {
    id: 4,
    name: '智能手机',
    category: '家电',
    price: 4999.00,
    stock: 200,
    status: true
  },
  {
    id: 5,
    name: '女士连衣裙',
    category: '服装',
    price: 299.00,
    stock: 150,
    status: true
  }
])

// 商品列表数据
const productList = ref([])
const total = ref(0)
const categoryOptions = ref([])
const selectedProducts = ref([])

// 对话框状态
const batchDialogVisible = ref(false)
const importExportDialogVisible = ref(false)
const importExportTab = ref('import')

// 批量操作表单
const batchForm = reactive({
  operation: '',
  tags: [],
  categoryId: null
})

// 导出表单
const exportForm = reactive({
  type: 'all'
})

// 获取商品列表
const fetchProductList = () => {
  loading.value = true
  // 模拟API请求
  setTimeout(() => {
    // 模拟数据
    productList.value = Array.from({ length: 10 }).map((_, index) => ({
      id: index + 1,
      name: `测试商品${index + 1}`,
      cover: 'https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png',
      categoryName: index % 3 === 0 ? '服装' : index % 3 === 1 ? '鞋包' : '配饰',
      price: Math.random() * 1000 + 10,
      stock: Math.floor(Math.random() * 1000),
      sales: Math.floor(Math.random() * 500),
      status: Math.random() > 0.3 ? 1 : 0,
      tags: ['hot', 'new', 'recommend'].filter(() => Math.random() > 0.5)
    }))
    total.value = 100
    loading.value = false
  }, 500)
}

// 获取商品分类
const fetchCategories = () => {
  // 模拟API请求
  setTimeout(() => {
    categoryOptions.value = [
      {
        value: 1,
        label: '服装',
        children: [
          {
            value: 3,
            label: '男装',
            children: [
              { value: 7, label: 'T恤' },
              { value: 8, label: '衬衫' }
            ]
          },
          {
            value: 4,
            label: '女装',
            children: [
              { value: 9, label: '连衣裙' },
              { value: 10, label: '上衣' }
            ]
          }
        ]
      },
      {
        value: 2,
        label: '鞋包',
        children: [
          { value: 5, label: '男鞋' },
          { value: 6, label: '女鞋' }
        ]
      }
    ]
  }, 300)
}

// 搜索
const handleSearch = () => {
  pagination.currentPage = 1
  fetchProductList()
}

// 重置搜索
const resetSearch = () => {
  searchForm.name = ''
  searchForm.category = ''
  handleSearch()
}

// 表格选择变化
const handleSelectionChange = (selection) => {
  selectedProducts.value = selection
}

// 状态切换
const handleToggleStatus = (row) => {
  row.status = !row.status
}

// 添加商品
const handleAdd = () => {
  router.push('/product/add')
}

// 编辑商品
const handleEdit = (row) => {
  router.push(`/product/edit/${row.id}`)
}

// 复制商品
const handleCopy = (row) => {
  ElMessageBox.confirm(`确定要复制"${row.name}"商品吗?`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'info'
  }).then(() => {
    // 模拟API请求
    setTimeout(() => {
      ElMessage.success('复制成功')
      fetchProductList()
    }, 300)
  }).catch(() => {})
}

// 删除商品
const handleDelete = (row) => {
  ElMessageBox.confirm(`确定要删除"${row.name}"商品吗?`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 模拟API请求
    setTimeout(() => {
      ElMessage.success('删除成功')
      fetchProductList()
    }, 300)
  }).catch(() => {})
}

// 批量操作
const handleBatchOperation = () => {
  if (selectedProducts.value.length === 0) {
    ElMessage.warning('请选择需要操作的商品')
    return
  }
  
  batchForm.operation = ''
  batchForm.tags = []
  batchForm.categoryId = null
  batchDialogVisible.value = true
}

// 批量操作确认
const handleBatchConfirm = () => {
  if (!batchForm.operation) {
    ElMessage.warning('请选择操作类型')
    return
  }
  
  if (batchForm.operation === '标签' && batchForm.tags.length === 0) {
    ElMessage.warning('请至少选择一个标签')
    return
  }
  
  if (batchForm.operation === '分类' && !batchForm.categoryId) {
    ElMessage.warning('请选择商品分类')
    return
  }
  
  if (batchForm.operation === '删除') {
    ElMessageBox.confirm(`确定要删除选中的${selectedProducts.value.length}个商品吗?`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      executeBatchOperation()
    }).catch(() => {})
  } else {
    executeBatchOperation()
  }
}

// 执行批量操作
const executeBatchOperation = () => {
  batchLoading.value = true
  
  // 模拟API请求
  setTimeout(() => {
    ElMessage.success(`批量${batchForm.operation}操作成功`)
    batchDialogVisible.value = false
    batchLoading.value = false
    fetchProductList()
  }, 500)
}

// 导入导出
const handleImportExport = () => {
  importExportTab.value = 'import'
  importExportDialogVisible.value = true
}

// 文件变化
const handleFileChange = (file) => {
  console.log('Selected file:', file)
}

// 下载导入模板
const handleDownloadTemplate = () => {
  ElMessage.success('下载导入模板成功')
}

// 导入
const handleImport = () => {
  importLoading.value = true
  
  // 模拟API请求
  setTimeout(() => {
    ElMessage.success('导入商品成功')
    importLoading.value = false
    importExportDialogVisible.value = false
    fetchProductList()
  }, 1000)
}

// 导出
const handleExport = () => {
  exportLoading.value = true
  
  // 模拟API请求
  setTimeout(() => {
    ElMessage.success('导出商品成功')
    exportLoading.value = false
    importExportDialogVisible.value = false
  }, 1000)
}

// 分页大小变化
const handleSizeChange = (size) => {
  pagination.pageSize = size
  fetchProductList()
}

// 页数变化
const handleCurrentChange = (page) => {
  pagination.currentPage = page
  fetchProductList()
}

// 初始化
onMounted(() => {
  fetchCategories()
  fetchProductList()
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

.filter-container {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.import-export-dialog {
  min-height: 250px;
}
</style> 