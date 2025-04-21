<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>操作日志</span>
        </div>
      </template>
      
      <div class="filter-container">
        <el-input
          v-model="listQuery.username"
          placeholder="操作人"
          style="width: 200px;"
          class="filter-item"
          clearable
        />
        <el-select
          v-model="listQuery.operationType"
          placeholder="操作类型"
          clearable
          class="filter-item"
          style="width: 130px"
        >
          <el-option v-for="item in operationOptions" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          class="filter-item"
          style="width: 340px"
        />
        <el-button type="primary" icon="Search" @click="handleFilter">搜索</el-button>
        <el-button icon="Refresh" @click="resetFilter">重置</el-button>
        <el-button type="danger" icon="Delete" @click="handleDelete">删除选中</el-button>
      </div>
      
      <el-table
        v-loading="listLoading"
        :data="list"
        border
        fit
        highlight-current-row
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column label="ID" prop="id" align="center" width="80">
          <template #default="scope">
            <span>{{ scope.row.id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作人" width="120" align="center">
          <template #default="scope">
            <span>{{ scope.row.username }}</span>
          </template>
        </el-table-column>
        <el-table-column label="IP地址" width="130" align="center">
          <template #default="scope">
            <span>{{ scope.row.ip }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作类型" width="120" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.operationType | operationTypeFilter">{{ scope.row.operationType }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作内容" min-width="200" align="center">
          <template #default="scope">
            <span>{{ scope.row.content }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作时间" width="160" align="center">
          <template #default="scope">
            <span>{{ scope.row.createTime }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作模块" width="120" align="center">
          <template #default="scope">
            <span>{{ scope.row.module }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="120" class-name="small-padding fixed-width">
          <template #default="scope">
            <el-button size="small" type="info" @click="handleDetail(scope.row)">
              详情
            </el-button>
            <el-button size="small" type="danger" @click="handleDeleteSingle(scope.row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <pagination
        v-show="total > 0"
        :total="total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="fetchData"
      />
    </el-card>
    
    <!-- 日志详情对话框 -->
    <el-dialog title="日志详情" :visible.sync="dialogVisible" width="600px">
      <el-descriptions title="操作信息" :column="1" border>
        <el-descriptions-item label="操作人">{{ currentLog.username }}</el-descriptions-item>
        <el-descriptions-item label="操作时间">{{ currentLog.createTime }}</el-descriptions-item>
        <el-descriptions-item label="IP地址">{{ currentLog.ip }}</el-descriptions-item>
        <el-descriptions-item label="操作类型">{{ currentLog.operationType }}</el-descriptions-item>
        <el-descriptions-item label="操作模块">{{ currentLog.module }}</el-descriptions-item>
        <el-descriptions-item label="操作内容">{{ currentLog.content }}</el-descriptions-item>
        <el-descriptions-item label="操作结果">{{ currentLog.result }}</el-descriptions-item>
        <el-descriptions-item label="浏览器">{{ currentLog.browser }}</el-descriptions-item>
        <el-descriptions-item label="操作系统">{{ currentLog.os }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script>
import { defineComponent, ref, reactive, toRefs } from 'vue'
import Pagination from '@/components/Pagination'

export default defineComponent({
  name: 'SystemLog',
  components: { Pagination },
  setup() {
    const state = reactive({
      list: [
        {
          id: 1,
          username: 'admin',
          ip: '192.168.1.1',
          operationType: '新增',
          content: '新增商品：iPhone 14 Pro',
          createTime: '2023-05-12 10:23:45',
          module: '商品管理',
          result: '成功',
          browser: 'Chrome 112.0.0.0',
          os: 'Windows 10'
        },
        {
          id: 2,
          username: 'manager',
          ip: '192.168.1.2',
          operationType: '修改',
          content: '修改用户信息：user001',
          createTime: '2023-05-11 16:44:12',
          module: '用户管理',
          result: '成功',
          browser: 'Firefox 113.0',
          os: 'MacOS 12.4'
        },
        {
          id: 3,
          username: 'admin',
          ip: '192.168.1.1',
          operationType: '删除',
          content: '删除订单：OR202305100045',
          createTime: '2023-05-10 09:12:34',
          module: '订单管理',
          result: '成功',
          browser: 'Chrome 112.0.0.0',
          os: 'Windows 10'
        }
      ],
      total: 3,
      listLoading: false,
      listQuery: {
        page: 1,
        limit: 10,
        username: '',
        operationType: ''
      },
      operationOptions: [
        { value: '新增', label: '新增' },
        { value: '修改', label: '修改' },
        { value: '删除', label: '删除' },
        { value: '查询', label: '查询' },
        { value: '登录', label: '登录' },
        { value: '退出', label: '退出' }
      ],
      dateRange: [],
      dialogVisible: false,
      currentLog: {},
      selectedLogs: []
    })
    
    const fetchData = () => {
      state.listLoading = true
      // 模拟API请求
      setTimeout(() => {
        state.listLoading = false
      }, 500)
    }
    
    const handleFilter = () => {
      state.listQuery.page = 1
      fetchData()
    }
    
    const resetFilter = () => {
      state.listQuery.username = ''
      state.listQuery.operationType = ''
      state.dateRange = []
      fetchData()
    }
    
    const handleDetail = (row) => {
      state.currentLog = row
      state.dialogVisible = true
    }
    
    const handleSelectionChange = (selection) => {
      state.selectedLogs = selection
    }
    
    const handleDeleteSingle = (row) => {
      // 删除单条日志
    }
    
    const handleDelete = () => {
      // 批量删除日志
    }
    
    return {
      ...toRefs(state),
      fetchData,
      handleFilter,
      resetFilter,
      handleDetail,
      handleSelectionChange,
      handleDeleteSingle,
      handleDelete
    }
  }
})
</script>

<style scoped>
.filter-container {
  padding-bottom: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.filter-item {
  margin-right: 10px;
}
</style> 