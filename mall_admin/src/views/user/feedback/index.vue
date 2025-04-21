<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>用户反馈</span>
        </div>
      </template>
      
      <div class="filter-container">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="反馈类型">
            <el-select v-model="searchForm.type" placeholder="请选择类型" clearable>
              <el-option label="功能建议" value="suggestion"></el-option>
              <el-option label="产品问题" value="problem"></el-option>
              <el-option label="内容纠错" value="correction"></el-option>
              <el-option label="其他" value="other"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="处理状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
              <el-option label="待处理" value="pending"></el-option>
              <el-option label="处理中" value="processing"></el-option>
              <el-option label="已解决" value="resolved"></el-option>
              <el-option label="已关闭" value="closed"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <el-table :data="feedbackList" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="user" label="用户" width="120">
          <template #default="scope">
            {{ scope.row.userName }}
          </template>
        </el-table-column>
        <el-table-column prop="type" label="反馈类型" width="120">
          <template #default="scope">
            <el-tag :type="getFeedbackTypeTag(scope.row.type)">{{ getFeedbackTypeText(scope.row.type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="反馈标题" min-width="200"></el-table-column>
        <el-table-column prop="content" label="反馈内容" min-width="300" show-overflow-tooltip></el-table-column>
        <el-table-column prop="createTime" label="反馈时间" width="180"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getFeedbackStatusTag(scope.row.status)">{{ getFeedbackStatusText(scope.row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button size="small" @click="handleReply(scope.row)">回复</el-button>
            <el-button size="small" type="danger" @click="handleClose(scope.row)" v-if="scope.row.status !== 'closed'">关闭</el-button>
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
    
    <!-- 回复对话框 -->
    <el-dialog v-model="replyDialogVisible" title="回复反馈" width="600px">
      <div class="feedback-detail" v-if="currentFeedback">
        <div class="feedback-detail-item">
          <span class="label">反馈用户：</span>
          <span>{{ currentFeedback.userName }}</span>
        </div>
        <div class="feedback-detail-item">
          <span class="label">反馈类型：</span>
          <el-tag :type="getFeedbackTypeTag(currentFeedback.type)">{{ getFeedbackTypeText(currentFeedback.type) }}</el-tag>
        </div>
        <div class="feedback-detail-item">
          <span class="label">反馈标题：</span>
          <span>{{ currentFeedback.title }}</span>
        </div>
        <div class="feedback-detail-item content">
          <span class="label">反馈内容：</span>
          <div class="content-box">{{ currentFeedback.content }}</div>
        </div>
        
        <div class="feedback-images" v-if="currentFeedback.images && currentFeedback.images.length > 0">
          <div class="label">附件图片：</div>
          <div class="image-list">
            <el-image 
              v-for="(image, index) in currentFeedback.images" 
              :key="index"
              :src="image"
              :preview-src-list="currentFeedback.images"
              style="width: 100px; height: 100px; margin-right: 10px; margin-bottom: 10px"
            ></el-image>
          </div>
        </div>
        
        <div class="reply-history" v-if="currentFeedback.replies && currentFeedback.replies.length > 0">
          <div class="label">历史回复：</div>
          <div class="reply-item" v-for="(reply, index) in currentFeedback.replies" :key="index">
            <div class="reply-info">
              <span class="reply-user">{{ reply.adminName }}</span>
              <span class="reply-time">{{ reply.replyTime }}</span>
            </div>
            <div class="reply-content">{{ reply.content }}</div>
          </div>
        </div>
        
        <div class="reply-form">
          <div class="label">回复内容：</div>
          <el-input 
            v-model="replyForm.content" 
            type="textarea" 
            :rows="4" 
            placeholder="请输入回复内容" 
          ></el-input>
        </div>
        
        <div class="status-form">
          <div class="label">更新状态：</div>
          <el-radio-group v-model="replyForm.status">
            <el-radio label="processing">处理中</el-radio>
            <el-radio label="resolved">已解决</el-radio>
            <el-radio label="closed">关闭</el-radio>
          </el-radio-group>
        </div>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="replyDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmitReply" :loading="replyLoading">提交回复</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

// 加载状态
const loading = ref(false)
const replyLoading = ref(false)

// 搜索表单
const searchForm = reactive({
  type: '',
  status: ''
})

// 分页信息
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 50
})

// 反馈列表
const feedbackList = ref([
  {
    id: 1,
    userId: 1001,
    userName: '张三',
    type: 'suggestion',
    title: '关于购物车功能的建议',
    content: '希望能够增加购物车商品的批量删除功能，现在一个个删除太麻烦了。',
    createTime: '2023-06-10 14:30:25',
    status: 'pending',
    images: [],
    replies: []
  },
  {
    id: 2,
    userId: 1002,
    userName: '李四',
    type: 'problem',
    title: '商品详情页图片加载失败',
    content: '在查看某些商品详情时，产品图片无法正常加载，显示破损图标。',
    createTime: '2023-06-09 09:12:36',
    status: 'processing',
    images: [''],
    replies: [
      {
        adminId: 1,
        adminName: '管理员A',
        content: '您好，我们已经收到您的反馈，正在处理中。请问您使用的是什么设备和浏览器版本？',
        replyTime: '2023-06-09 10:25:18'
      }
    ]
  },
  {
    id: 3,
    userId: 1003,
    userName: '王五',
    type: 'correction',
    title: '商品描述错误',
    content: '商品ID为10086的产品，描述中提到"7天无理由退货"，但实际下单后客服说不支持无理由退货。',
    createTime: '2023-06-08 16:45:03',
    status: 'resolved',
    images: [],
    replies: [
      {
        adminId: 2,
        adminName: '管理员B',
        content: '感谢您的反馈，我们已经核实并修正了这个错误。现在该商品已更新为"不支持7天无理由退货"的说明。',
        replyTime: '2023-06-08 17:30:42'
      }
    ]
  },
  {
    id: 4,
    userId: 1004,
    userName: '赵六',
    type: 'other',
    title: '配送问题咨询',
    content: '请问商城是否支持指定时间段配送？我白天不在家，希望能够安排晚上配送。',
    createTime: '2023-06-07 11:20:15',
    status: 'closed',
    images: [],
    replies: [
      {
        adminId: 1,
        adminName: '管理员A',
        content: '您好，目前我们的配送时间可以选择上午或下午，暂不支持晚间配送。建议您可以选择工作日下午配送，或使用自提服务。',
        replyTime: '2023-06-07 13:05:27'
      }
    ]
  }
])

// 对话框相关
const replyDialogVisible = ref(false)
const currentFeedback = ref(null)
const replyForm = reactive({
  content: '',
  status: 'processing'
})

// 获取反馈类型文本
const getFeedbackTypeText = (type) => {
  const types = {
    'suggestion': '功能建议',
    'problem': '产品问题',
    'correction': '内容纠错',
    'other': '其他'
  }
  return types[type] || '未知'
}

// 获取反馈类型标签样式
const getFeedbackTypeTag = (type) => {
  const tags = {
    'suggestion': 'success',
    'problem': 'danger',
    'correction': 'warning',
    'other': 'info'
  }
  return tags[type] || 'info'
}

// 获取反馈状态文本
const getFeedbackStatusText = (status) => {
  const statuses = {
    'pending': '待处理',
    'processing': '处理中',
    'resolved': '已解决',
    'closed': '已关闭'
  }
  return statuses[status] || '未知'
}

// 获取反馈状态标签样式
const getFeedbackStatusTag = (status) => {
  const tags = {
    'pending': 'info',
    'processing': 'warning',
    'resolved': 'success',
    'closed': 'default'
  }
  return tags[status] || 'info'
}

// 加载数据
const fetchFeedbackList = () => {
  loading.value = true
  // 模拟API请求
  setTimeout(() => {
    loading.value = false
  }, 500)
}

// 搜索
const handleSearch = () => {
  pagination.currentPage = 1
  fetchFeedbackList()
}

// 重置搜索
const resetSearch = () => {
  searchForm.type = ''
  searchForm.status = ''
  handleSearch()
}

// 回复反馈
const handleReply = (row) => {
  currentFeedback.value = { ...row }
  replyForm.content = ''
  replyForm.status = row.status === 'pending' ? 'processing' : row.status
  replyDialogVisible.value = true
}

// 关闭反馈
const handleClose = (row) => {
  console.log('关闭反馈', row)
  // 实际项目中应该调用API
  row.status = 'closed'
}

// 提交回复
const handleSubmitReply = () => {
  if (!replyForm.content.trim()) {
    alert('请输入回复内容')
    return
  }
  
  replyLoading.value = true
  
  // 模拟API请求
  setTimeout(() => {
    // 添加回复
    const now = new Date()
    const replyTime = now.getFullYear() + '-' +
      String(now.getMonth() + 1).padStart(2, '0') + '-' +
      String(now.getDate()).padStart(2, '0') + ' ' +
      String(now.getHours()).padStart(2, '0') + ':' +
      String(now.getMinutes()).padStart(2, '0') + ':' +
      String(now.getSeconds()).padStart(2, '0')
    
    if (!currentFeedback.value.replies) {
      currentFeedback.value.replies = []
    }
    
    currentFeedback.value.replies.push({
      adminId: 1,
      adminName: '管理员A',
      content: replyForm.content,
      replyTime: replyTime
    })
    
    // 更新状态
    currentFeedback.value.status = replyForm.status
    
    // 更新原列表中的数据
    const index = feedbackList.value.findIndex(item => item.id === currentFeedback.value.id)
    if (index !== -1) {
      feedbackList.value[index] = { ...currentFeedback.value }
    }
    
    replyLoading.value = false
    replyDialogVisible.value = false
  }, 500)
}

// 分页大小变化
const handleSizeChange = (size) => {
  pagination.pageSize = size
  fetchFeedbackList()
}

// 页数变化
const handleCurrentChange = (page) => {
  pagination.currentPage = page
  fetchFeedbackList()
}

// 初始化
fetchFeedbackList()
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.filter-container {
  margin-bottom: 20px;
}
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
.feedback-detail {
  margin-bottom: 20px;
}
.feedback-detail-item {
  margin-bottom: 12px;
  display: flex;
}
.feedback-detail-item.content {
  align-items: flex-start;
}
.feedback-detail .label {
  font-weight: bold;
  min-width: 80px;
  margin-right: 10px;
}
.content-box {
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 4px;
  flex: 1;
}
.feedback-images {
  margin-top: 15px;
  margin-bottom: 15px;
}
.image-list {
  display: flex;
  flex-wrap: wrap;
  margin-top: 10px;
}
.reply-history {
  margin-top: 20px;
  margin-bottom: 20px;
}
.reply-item {
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 10px;
}
.reply-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}
.reply-user {
  font-weight: bold;
}
.reply-time {
  color: #909399;
  font-size: 12px;
}
.reply-form, .status-form {
  margin-top: 20px;
}
</style> 