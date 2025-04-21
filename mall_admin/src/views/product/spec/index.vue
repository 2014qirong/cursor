<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>规格管理</span>
          <el-button type="primary" size="small" @click="handleAddSpec">添加规格</el-button>
        </div>
      </template>
      
      <el-table :data="specList" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="规格名称"></el-table-column>
        <el-table-column prop="values" label="规格值">
          <template #default="scope">
            <el-tag 
              v-for="item in scope.row.values" 
              :key="item" 
              style="margin-right: 5px; margin-bottom: 5px;"
            >
              {{ item }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="handleEditSpec(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDeleteSpec(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 规格表单对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="specForm" label-width="100px">
        <el-form-item label="规格名称">
          <el-input v-model="specForm.name" placeholder="请输入规格名称"></el-input>
        </el-form-item>
        <el-form-item label="规格值">
          <el-tag 
            v-for="(tag, index) in specForm.values" 
            :key="index" 
            closable 
            :disable-transitions="false" 
            @close="handleRemoveTag(tag)"
            style="margin-right: 5px; margin-bottom: 5px;"
          >
            {{ tag }}
          </el-tag>
          <el-input
            v-if="inputVisible"
            ref="InputRef"
            v-model="inputValue"
            class="input-new-tag"
            size="small"
            @keyup.enter="handleInputConfirm"
            @blur="handleInputConfirm"
          ></el-input>
          <el-button v-else class="button-new-tag" size="small" @click="showInput">+ 添加规格值</el-button>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmitSpec">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, nextTick } from 'vue'

const loading = ref(false)
const InputRef = ref(null)
const inputVisible = ref(false)
const inputValue = ref('')

// 规格列表
const specList = ref([
  {
    id: 1,
    name: '颜色',
    values: ['红色', '蓝色', '黑色', '白色']
  },
  {
    id: 2,
    name: '尺寸',
    values: ['S', 'M', 'L', 'XL', 'XXL']
  },
  {
    id: 3,
    name: '内存',
    values: ['64GB', '128GB', '256GB', '512GB']
  }
])

// 对话框相关
const dialogVisible = ref(false)
const dialogTitle = ref('添加规格')
const specForm = reactive({
  id: null,
  name: '',
  values: []
})

// 添加规格
const handleAddSpec = () => {
  dialogTitle.value = '添加规格'
  specForm.id = null
  specForm.name = ''
  specForm.values = []
  dialogVisible.value = true
}

// 编辑规格
const handleEditSpec = (row) => {
  dialogTitle.value = '编辑规格'
  specForm.id = row.id
  specForm.name = row.name
  specForm.values = [...row.values]
  dialogVisible.value = true
}

// 删除规格
const handleDeleteSpec = (row) => {
  // TODO: 实现删除逻辑
  console.log('删除规格', row)
}

// 提交规格表单
const handleSubmitSpec = () => {
  // TODO: 实现保存逻辑
  console.log('保存规格', specForm)
  dialogVisible.value = false
}

// 删除标签
const handleRemoveTag = (tag) => {
  specForm.values.splice(specForm.values.indexOf(tag), 1)
}

// 显示输入框
const showInput = () => {
  inputVisible.value = true
  nextTick(() => {
    InputRef.value.focus()
  })
}

// 输入确认
const handleInputConfirm = () => {
  if (inputValue.value) {
    specForm.values.push(inputValue.value)
  }
  inputVisible.value = false
  inputValue.value = ''
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.input-new-tag {
  width: 90px;
  margin-right: 5px;
  vertical-align: bottom;
}
</style> 