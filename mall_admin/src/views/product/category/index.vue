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
        <el-table :data="tableData" style="width: 100%" row-key="id" border default-expand-all>
          <el-table-column prop="name" label="分类名称"></el-table-column>
          <el-table-column prop="sort" label="排序" width="120"></el-table-column>
          <el-table-column prop="status" label="状态" width="120">
            <template #default="scope">
              <el-tag :type="scope.row.status ? 'success' : 'danger'">
                {{ scope.row.status ? '启用' : '禁用' }}
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
    <el-dialog v-model="dialogVisible" :title="dialogTitle">
      <el-form :model="form" label-width="100px">
        <el-form-item label="分类名称">
          <el-input v-model="form.name" placeholder="请输入分类名称"></el-input>
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.sort" :min="0" :step="1"></el-input-number>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="form.status" :active-value="true" :inactive-value="false"></el-switch>
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
import { ref } from 'vue'

const tableData = ref([
  {
    id: 1,
    name: '家电',
    sort: 1,
    status: true,
    children: [
      {
        id: 11,
        name: '电视',
        sort: 1,
        status: true
      },
      {
        id: 12,
        name: '冰箱',
        sort: 2,
        status: true
      }
    ]
  },
  {
    id: 2,
    name: '服装',
    sort: 2,
    status: true,
    children: [
      {
        id: 21,
        name: '男装',
        sort: 1,
        status: true
      },
      {
        id: 22,
        name: '女装',
        sort: 2,
        status: true
      }
    ]
  },
  {
    id: 3,
    name: '食品',
    sort: 3,
    status: false
  }
])

const dialogVisible = ref(false)
const dialogTitle = ref('添加分类')
const form = ref({
  id: null,
  name: '',
  sort: 0,
  status: true
})

const handleAdd = () => {
  dialogTitle.value = '添加分类'
  form.value = {
    id: null,
    name: '',
    sort: 0,
    status: true
  }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑分类'
  form.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = (row) => {
  // TODO: 实现删除逻辑
  console.log('删除分类', row)
}

const handleSubmit = () => {
  // TODO: 实现提交逻辑
  console.log('提交分类', form.value)
  dialogVisible.value = false
}
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
</style>