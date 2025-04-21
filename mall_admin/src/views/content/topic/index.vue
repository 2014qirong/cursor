<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>专题页管理</span>
          <el-button type="primary" icon="Plus" @click="handleCreateTopic">新建专题</el-button>
        </div>
      </template>
      
      <div class="filter-container">
        <el-input
          v-model="listQuery.title"
          placeholder="专题标题"
          style="width: 200px;"
          class="filter-item"
          clearable
          @keyup.enter="handleFilter"
        />
        <el-select
          v-model="listQuery.status"
          placeholder="状态"
          clearable
          style="width: 120px"
          class="filter-item"
        >
          <el-option v-for="item in statusOptions" :key="item.value" :label="item.label" :value="item.value" />
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
      </div>
      
      <el-table
        v-loading="listLoading"
        :data="list"
        border
        fit
        highlight-current-row
        style="width: 100%"
      >
        <el-table-column label="ID" align="center" width="80">
          <template #default="scope">
            <span>{{ scope.row.id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="专题图片" width="120" align="center">
          <template #default="scope">
            <el-image 
              :src="scope.row.image" 
              :preview-src-list="[scope.row.image]"
              style="width: 80px; height: 44px"
              fit="cover"
            />
          </template>
        </el-table-column>
        <el-table-column label="专题标题" min-width="180">
          <template #default="scope">
            <router-link :to="'/content/topic/edit/'+scope.row.id" class="link-type">
              <span>{{ scope.row.title }}</span>
            </router-link>
          </template>
        </el-table-column>
        <el-table-column label="子标题" min-width="150">
          <template #default="scope">
            <span>{{ scope.row.subtitle }}</span>
          </template>
        </el-table-column>
        <el-table-column label="商品数量" width="100" align="center">
          <template #default="scope">
            <span>{{ scope.row.productCount }}</span>
          </template>
        </el-table-column>
        <el-table-column label="阅读量" width="100" align="center">
          <template #default="scope">
            <span>{{ scope.row.readCount }}</span>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" width="160" align="center">
          <template #default="scope">
            <span>{{ scope.row.createTime }}</span>
          </template>
        </el-table-column>
        <el-table-column label="更新时间" width="160" align="center">
          <template #default="scope">
            <span>{{ scope.row.updateTime }}</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.status === '已发布' ? 'success' : 'info'">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="250" class-name="small-padding fixed-width">
          <template #default="scope">
            <el-button
              size="small"
              type="primary"
              @click="handleUpdate(scope.row)"
            >
              编辑
            </el-button>
            <el-button
              v-if="scope.row.status === '草稿'"
              size="small"
              type="success"
              @click="handlePublish(scope.row)"
            >
              发布
            </el-button>
            <el-button
              v-if="scope.row.status === '已发布'"
              size="small"
              type="warning"
              @click="handleOffline(scope.row)"
            >
              下线
            </el-button>
            <el-button
              size="small"
              type="danger"
              @click="handleDelete(scope.row)"
            >
              删除
            </el-button>
            <el-button
              size="small"
              type="info"
              @click="handlePreview(scope.row)"
            >
              预览
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <pagination
        v-show="total > 0"
        :total="total"
        v-model:page="listQuery.page"
        v-model:limit="listQuery.limit"
        @pagination="getList"
      />
    </el-card>
    
    <!-- 专题表单对话框 -->
    <el-dialog
      :title="textMap[dialogStatus]"
      v-model="dialogFormVisible"
      width="650px"
    >
      <el-form
        ref="dataForm"
        :model="temp"
        label-position="right"
        label-width="100px"
        :rules="rules"
      >
        <el-form-item label="专题标题" prop="title">
          <el-input v-model="temp.title" placeholder="请输入专题标题" />
        </el-form-item>
        <el-form-item label="子标题" prop="subtitle">
          <el-input v-model="temp.subtitle" placeholder="请输入子标题" />
        </el-form-item>
        <el-form-item label="专题图片" prop="image">
          <el-upload
            class="avatar-uploader"
            action="/api/upload"
            :show-file-list="false"
            :on-success="handleImageSuccess"
            :before-upload="beforeImageUpload"
          >
            <img v-if="temp.image" :src="temp.image" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
          <div class="image-tip">图片尺寸建议：1200 x 660 像素，支持 jpg、png 格式</div>
        </el-form-item>
        <el-form-item label="专题描述">
          <el-input type="textarea" v-model="temp.description" :rows="3" placeholder="请输入专题描述" />
        </el-form-item>
        <el-form-item label="排序值" prop="sort">
          <el-input-number v-model="temp.sort" :min="0" :max="999" />
          <span class="sort-tip">值越小排序越靠前</span>
        </el-form-item>
        <el-form-item label="是否显示">
          <el-switch v-model="temp.isShow" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取消</el-button>
          <el-button type="primary" @click="dialogStatus === 'create' ? createData() : updateData()">
            确认
          </el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- 专题预览对话框 -->
    <el-dialog
      title="专题预览"
      v-model="previewVisible"
      width="800px"
      class="preview-dialog"
    >
      <div class="topic-preview">
        <div class="topic-header">
          <div class="topic-title">{{ currentTopic.title }}</div>
          <div class="topic-subtitle">{{ currentTopic.subtitle }}</div>
        </div>
        <div class="topic-image">
          <el-image :src="currentTopic.image" fit="cover" />
        </div>
        <div class="topic-description">
          {{ currentTopic.description }}
        </div>
        <div class="topic-products-title">专题商品</div>
        <div class="topic-products">
          <div v-for="(product, index) in currentTopic.products" :key="index" class="product-item">
            <div class="product-image">
              <el-image :src="product.image" fit="cover" />
            </div>
            <div class="product-name">{{ product.name }}</div>
            <div class="product-price">¥{{ product.price }}</div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { defineComponent, ref, reactive, toRefs, nextTick } from 'vue'
import Pagination from '@/components/Pagination/index.vue'

export default defineComponent({
  name: 'ContentTopic',
  components: { Pagination },
  setup() {
    const dataForm = ref(null)
    
    const state = reactive({
      list: [
        {
          id: 1,
          title: '夏日清凉特辑',
          subtitle: '解锁夏日清凉新方式',
          image: 'https://placeholder.pics/svg/600x330/DEDEDE/555555/夏日清凉特辑',
          description: '炎炎夏日，让这些清凉好物陪你度过每一天，从家电到饮品，从穿搭到户外，满足你的一切夏日所需。',
          productCount: 24,
          readCount: 1254,
          createTime: '2023-04-15 10:23:45',
          updateTime: '2023-04-18 15:30:12',
          status: '已发布',
          sort: 5,
          isShow: true,
          products: [
            { 
              id: 101, 
              name: '便携式小风扇', 
              image: 'https://placeholder.pics/svg/200x200', 
              price: 39.90 
            },
            { 
              id: 102, 
              name: '冰丝凉席三件套', 
              image: 'https://placeholder.pics/svg/200x200', 
              price: 199.00 
            },
            { 
              id: 103, 
              name: '夏日冰镇饮料杯', 
              image: 'https://placeholder.pics/svg/200x200', 
              price: 29.90 
            }
          ]
        },
        {
          id: 2,
          title: '智能家居全屋方案',
          subtitle: '打造智慧生活新体验',
          image: 'https://placeholder.pics/svg/600x330/DEDEDE/555555/智能家居',
          description: '从智能音箱到安防监控，从智能灯具到智能厨电，一站式满足你的智能家居需求，让生活更便捷、更舒适。',
          productCount: 36,
          readCount: 2187,
          createTime: '2023-03-25 14:18:32',
          updateTime: '2023-04-10 09:42:51',
          status: '已发布',
          sort: 3,
          isShow: true,
          products: [
            { 
              id: 201, 
              name: '智能音箱', 
              image: 'https://placeholder.pics/svg/200x200', 
              price: 299.00 
            },
            { 
              id: 202, 
              name: '智能门锁', 
              image: 'https://placeholder.pics/svg/200x200', 
              price: 1299.00 
            }
          ]
        },
        {
          id: 3,
          title: '健身器材精选',
          subtitle: '在家也能练出好身材',
          image: 'https://placeholder.pics/svg/600x330/DEDEDE/555555/健身器材',
          description: '精选家用健身器材，从哑铃到跑步机，从瑜伽垫到健身环，助你在家也能拥有专业健身体验。',
          productCount: 18,
          readCount: 876,
          createTime: '2023-05-06 16:35:28',
          updateTime: '2023-05-06 16:35:28',
          status: '草稿',
          sort: 8,
          isShow: false,
          products: [
            { 
              id: 301, 
              name: '多功能健身器', 
              image: 'https://placeholder.pics/svg/200x200', 
              price: 799.00 
            }
          ]
        }
      ],
      total: 3,
      listLoading: false,
      listQuery: {
        page: 1,
        limit: 10,
        title: '',
        status: ''
      },
      statusOptions: [
        { label: '全部', value: '' },
        { label: '已发布', value: '已发布' },
        { label: '草稿', value: '草稿' }
      ],
      dateRange: [],
      temp: {
        id: undefined,
        title: '',
        subtitle: '',
        image: '',
        description: '',
        sort: 0,
        isShow: true
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: '编辑专题',
        create: '创建专题'
      },
      rules: {
        title: [{ required: true, message: '专题标题不能为空', trigger: 'blur' }],
        image: [{ required: true, message: '专题图片不能为空', trigger: 'change' }]
      },
      previewVisible: false,
      currentTopic: {}
    })
    
    const getList = () => {
      state.listLoading = true
      // 模拟API请求
      setTimeout(() => {
        state.listLoading = false
      }, 500)
    }
    
    const resetTemp = () => {
      state.temp = {
        id: undefined,
        title: '',
        subtitle: '',
        image: '',
        description: '',
        sort: 0,
        isShow: true
      }
    }
    
    const handleFilter = () => {
      state.listQuery.page = 1
      getList()
    }
    
    const resetFilter = () => {
      state.listQuery.title = ''
      state.listQuery.status = ''
      state.dateRange = []
      handleFilter()
    }
    
    const handleCreateTopic = () => {
      resetTemp()
      state.dialogStatus = 'create'
      state.dialogFormVisible = true
      nextTick(() => {
        if (dataForm.value) {
          dataForm.value.clearValidate()
        }
      })
    }
    
    const createData = () => {
      if (dataForm.value) {
        dataForm.value.validate((valid) => {
          if (valid) {
            state.dialogFormVisible = false
            // 创建专题逻辑
            state.temp.id = Date.now()
            state.temp.createTime = new Date().toLocaleString()
            state.temp.updateTime = new Date().toLocaleString()
            state.temp.status = '草稿'
            state.temp.productCount = 0
            state.temp.readCount = 0
            state.temp.products = []
            
            state.list.unshift(state.temp)
            state.total += 1
          }
        })
      }
    }
    
    const handleUpdate = (row) => {
      state.temp = Object.assign({}, row)
      state.dialogStatus = 'update'
      state.dialogFormVisible = true
      nextTick(() => {
        if (dataForm.value) {
          dataForm.value.clearValidate()
        }
      })
    }
    
    const updateData = () => {
      if (dataForm.value) {
        dataForm.value.validate((valid) => {
          if (valid) {
            state.dialogFormVisible = false
            // 更新专题逻辑
            const index = state.list.findIndex(v => v.id === state.temp.id)
            state.temp.updateTime = new Date().toLocaleString()
            state.list.splice(index, 1, state.temp)
          }
        })
      }
    }
    
    const handleDelete = (row) => {
      // 删除专题
      const index = state.list.findIndex(v => v.id === row.id)
      state.list.splice(index, 1)
      state.total -= 1
    }
    
    const handlePublish = (row) => {
      // 发布专题
      const index = state.list.findIndex(v => v.id === row.id)
      state.list[index].status = '已发布'
      state.list[index].updateTime = new Date().toLocaleString()
    }
    
    const handleOffline = (row) => {
      // 下线专题
      const index = state.list.findIndex(v => v.id === row.id)
      state.list[index].status = '草稿'
      state.list[index].updateTime = new Date().toLocaleString()
    }
    
    const handlePreview = (row) => {
      state.currentTopic = Object.assign({}, row)
      state.previewVisible = true
    }
    
    const handleImageSuccess = (response) => {
      // 图片上传成功
      state.temp.image = response.url
    }
    
    const beforeImageUpload = (file) => {
      // 图片上传前检查
      const isJPG = file.type === 'image/jpeg'
      const isPNG = file.type === 'image/png'
      const isLt2M = file.size / 1024 / 1024 < 2
      
      if (!isJPG && !isPNG) {
        // 显示错误提示
        return false
      }
      if (!isLt2M) {
        // 显示错误提示
        return false
      }
      return true
    }
    
    // 初始加载
    getList()
    
    return {
      dataForm,
      ...toRefs(state),
      getList,
      handleFilter,
      resetFilter,
      handleCreateTopic,
      createData,
      handleUpdate,
      updateData,
      handleDelete,
      handlePublish,
      handleOffline,
      handlePreview,
      handleImageSuccess,
      beforeImageUpload
    }
  }
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-container {
  padding-bottom: 18px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.filter-item {
  display: inline-block;
  vertical-align: middle;
  margin-right: 10px;
}

.link-type {
  color: #409EFF;
  text-decoration: none;
}

.link-type:hover {
  text-decoration: underline;
}

.avatar-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 178px;
  height: 98px;
}

.avatar-uploader:hover {
  border-color: #409EFF;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 98px;
  line-height: 98px;
  text-align: center;
}

.avatar {
  width: 178px;
  height: 98px;
  display: block;
  object-fit: cover;
}

.image-tip, .sort-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

.sort-tip {
  margin-left: 10px;
}

/* 专题预览样式 */
.topic-preview {
  max-width: 100%;
}

.topic-header {
  text-align: center;
  margin-bottom: 20px;
}

.topic-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 8px;
}

.topic-subtitle {
  font-size: 16px;
  color: #606266;
}

.topic-image {
  width: 100%;
  margin-bottom: 20px;
}

.topic-image .el-image {
  width: 100%;
  height: 330px;
}

.topic-description {
  font-size: 14px;
  line-height: 1.6;
  color: #606266;
  margin-bottom: 20px;
}

.topic-products-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #EBEEF5;
}

.topic-products {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.product-item {
  width: calc(33.33% - 10px);
  text-align: center;
}

.product-image {
  width: 100%;
  height: 150px;
  margin-bottom: 8px;
}

.product-image .el-image {
  width: 100%;
  height: 100%;
}

.product-name {
  font-size: 14px;
  margin-bottom: 5px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-price {
  font-size: 16px;
  color: #f56c6c;
  font-weight: bold;
}

@media (max-width: 768px) {
  .product-item {
    width: calc(50% - 10px);
  }
}
</style> 