<template>
  <!-- 页面容器 -->
  <div class="app-container">
    <!-- 使用Element Plus的卡片组件包装内容 -->
    <el-card class="box-card">
      <!-- 卡片头部插槽 -->
      <template #header>
        <div class="card-header">
          <span>订单统计</span>
        </div>
      </template>
      <!-- 图表容器，使用ref引用DOM元素 -->
      <div ref="chartRef" class="chart-container"></div>
    </el-card>
  </div>
</template>

<script setup>
// 导入Vue组合式API
import { ref, onMounted } from 'vue'
// 导入echarts图表库
import * as echarts from 'echarts'

// 创建图表DOM引用
const chartRef = ref(null)

// 组件挂载后初始化图表
onMounted(() => {
  if (chartRef.value) {
    // 初始化echarts实例
    const chart = echarts.init(chartRef.value)
    // 设置图表配置项
    chart.setOption({
      title: { text: '订单统计示例' }, // 图表标题
      tooltip: {}, // 启用提示框
      xAxis: { data: ['一月', '二月', '三月'] }, // X轴数据
      yAxis: {}, // Y轴配置
      series: [{ name: '订单量', type: 'bar', data: [120, 200, 150] }] // 数据系列配置
    })
  }
})
</script>

<style scoped>
/* 图表容器样式 */
.chart-container {
  width: 100%;
  height: 400px;
}
/* 卡片头部样式 */
.card-header {
  display: flex;
  align-items: center;
}
</style> 