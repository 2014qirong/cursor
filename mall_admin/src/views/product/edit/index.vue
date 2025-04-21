<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>编辑商品</span>
        </div>
      </template>
      <div class="product-edit">
        <el-form :model="form" label-width="120px">
          <el-form-item label="商品名称">
            <el-input v-model="form.name" placeholder="请输入商品名称"></el-input>
          </el-form-item>
          <el-form-item label="商品分类">
            <el-select v-model="form.category" placeholder="请选择商品分类">
              <el-option label="家电" value="appliance"></el-option>
              <el-option label="服装" value="clothing"></el-option>
              <el-option label="食品" value="food"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="商品价格">
            <el-input-number v-model="form.price" :min="0" :precision="2" :step="0.1"></el-input-number>
          </el-form-item>
          <el-form-item label="商品库存">
            <el-input-number v-model="form.stock" :min="0" :step="1"></el-input-number>
          </el-form-item>
          <el-form-item label="商品描述">
            <el-input type="textarea" v-model="form.description" placeholder="请输入商品描述"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSubmit">保存</el-button>
            <el-button @click="handleCancel">取消</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const productId = route.params.id

const form = ref({
  name: '',
  category: '',
  price: 0,
  stock: 0,
  description: ''
})

onMounted(() => {
  // 模拟获取商品数据
  form.value = {
    name: '测试商品' + productId,
    category: 'appliance',
    price: 199.99,
    stock: 100,
    description: '这是一个测试商品描述'
  }
})

const handleSubmit = () => {
  // TODO: 实现保存逻辑
  console.log('保存商品', form.value)
  router.push('/product/list')
}

const handleCancel = () => {
  router.go(-1)
}
</script>

<style scoped>
.product-edit {
  padding: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style> 