<template>
  <div class="pagination-container">
    <el-pagination
      v-model:currentPage="currentPage"
      v-model:pageSize="pageSize"
      :background="background"
      :layout="layout"
      :page-sizes="pageSizes"
      :total="total"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  total: {
    required: true,
    type: Number
  },
  page: {
    type: Number,
    default: 1
  },
  limit: {
    type: Number,
    default: 20
  },
  pageSizes: {
    type: Array,
    default() {
      return [10, 20, 30, 50]
    }
  },
  layout: {
    type: String,
    default: 'total, sizes, prev, pager, next, jumper'
  },
  background: {
    type: Boolean,
    default: true
  },
  hidden: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['pagination', 'update:page', 'update:limit'])

const currentPage = computed({
  get() {
    return props.page
  },
  set(val) {
    emit('update:page', val)
  }
})

const pageSize = computed({
  get() {
    return props.limit
  },
  set(val) {
    emit('update:limit', val)
  }
})

function handleSizeChange(val) {
  emit('pagination', { page: currentPage.value, limit: val })
  if (currentPage.value === 1) {
    // 当页数为1时，size改变，需要手动触发
    emit('pagination', { page: 1, limit: val })
  }
}

function handleCurrentChange(val) {
  emit('pagination', { page: val, limit: pageSize.value })
}
</script>

<style scoped>
.pagination-container {
  padding: 15px 0;
  text-align: right;
}
</style> 