<template>
  <div class="app-container">
    <div class="my-header search-wrapper">
      <el-card style="width: 1000px">
        <template #header>
          <div class="card-header">
            <div class="describe_word">工单</div>
            <el-form :inline="true" :model="searchData">
              <el-form-item prop="serviceId" label="老人id">
                <el-input v-model="searchData.member" placeholder="请输入" />
              </el-form-item>
              <el-form-item prop="orderId" label="服务者id">
                <el-input v-model="searchData.handler" placeholder="请输入" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" :icon="Search" @click="handleSearch">查询</el-button>
              </el-form-item>
            </el-form>

          </div>
        </template>
        <el-table :data="tableData" style="width: 100%" @selection-change="handleSelectionChange">
          <el-table-column type="selection" width="55" />
          <!-- <el-table-column label="Date" width="120">
                    <template #default="scope">{{ scope.row.date }}</template>
                  </el-table-column> -->
          <el-table-column property="orderId" label="工单号" width="200" />
          <el-table-column property="projectType" label="工单类型" width="200" />
          <el-table-column property="handler" label="服务者" width="200" />
          <el-table-column property="member" label="老人" width="200" />
          <!-- <el-table-column property="address" label="address" /> -->
        </el-table>
        <el-pagination class="content-center"  style="margin-top:20px ;" background :layout="paginationData.layout" 
                :total="paginationData.total" :page-size="paginationData.pageSize"
                :currentPage="paginationData.currentPage" @size-change="handleSizeChange"
                @current-change="handleCurrentChange" />
      </el-card>

      <el-card style="width: 650px">
        <template #header>
          <div class="card-header">
            <div class="describe_word">选定的工单</div>
            <el-button type="primary" :icon="Search" @click="detectOrder">检测工单</el-button>
          </div>

        </template>
        <el-table :data="selectedOrder" style="width: 100%">
          <el-table-column property="orderId" label="工单号" width="300" />
          <el-table-column property="projectType" label="工单类型" width="300" show-overflow-tooltip />
        </el-table>

      </el-card>
    </div>

    <el-card class="search-wrapper content-center">
      <v-chart class="chart" :option="option" />
    </el-card>

    <el-card class="search-wrapper">
      <div class="describe_word" style="margin-bottom: 10px;">工单详细结果</div>
      <el-tabs v-model="activeNameTab" class="demo-tabs" @tab-click="handleClick">
        <el-tab-pane label="工单号" disabled  > </el-tab-pane>
        <el-tab-pane v-for="(orderInfo, index) in exceptionOrder" :key="index" :label="orderInfo.id"
          :name="orderInfo.id">
          <div style="margin-bottom: 15px;">{{orderInfo.id}}号工单检测结果:
            <span style="color: #f67572;">异常工单</span>
          </div>
          <el-collapse v-model="activeNamesCollapse" @change="handleChange">
            <el-collapse-item v-for="(item, index) in orderInfo.error" :key="index" :title="item.key" :name="index">
              <div style="font-size: medium;">
                {{ item.value }}
              </div>
            </el-collapse-item>
          </el-collapse>
        </el-tab-pane>
      </el-tabs>
    </el-card>



  </div>
</template>

<script lang="ts" setup>
import { computed, ref, watch, onMounted } from 'vue'
import { Search } from "@element-plus/icons-vue"
import { reactive } from 'vue'
import * as echarts from 'echarts';
import VChart from 'vue-echarts';
import type { TabsPaneContext } from 'element-plus'
import axios from "axios"
import { ElMessage } from "element-plus"
import type { CollapseModelValue } from 'element-plus'
import { ElButton, ElDialog } from 'element-plus'
import { CircleCloseFilled } from '@element-plus/icons-vue'
import { usePagination } from "@/hooks/usePagination"

//单个异常工单信息
interface AbnormalInfo {
  key: string;
  value: string;
}

interface ErrorInfo {
  id: string;
  error: AbnormalInfo[];
}

interface OrderDetectResult {
  correct: number;
  suspect: number;
  error: number;
  suspect_info: any[];  // 根据实际需求定义类型
  error_info: ErrorInfo[];
}

interface OrderInfo {
  orderId: string,
  no: string,
  handler: string,
  member: string,
  serviceId: string,
  projectType: string,
  flag: number
}

interface PieDataItem {
  value: number;
  name: string;
  itemStyle: {
    color: string;
  };
}

const { paginationData, handleCurrentChange, handleSizeChange } = usePagination()

//搜索框
const searchData = reactive({
  member: "",//老人id
  handler: "",//服务者id
})
//分页工单
const tableData = ref<OrderInfo[]>([])
//选中的工单数组
const selectedOrder = ref<OrderInfo[]>()


const getOrderData = () => {
  axios({
    method: "get",
    url: `http://127.0.0.1:5555/work_order/list`,
    params: {
      currentPage: paginationData.currentPage,
      size: paginationData.pageSize,
      member: searchData.member || undefined,
      handler: searchData.handler || undefined,
    }
  }).then((res) => {
    paginationData.total = res.data.total
    tableData.value = res.data.list
  }).catch((error) => {
    console.error('Error fetching order data:', error)
    ElMessage.error('获取工单数据失败')
  })
}
//查询
const handleSearch = () =>{
  if (paginationData.currentPage === 1) {
    getOrderData()
  }
  // 当paginationData.currentPage发生改变时 , getOrderData会自动调用
  paginationData.currentPage = 1 
}
//当currentPage或pageSize发生变化时,调用getOrderData函数来获取新的数据;   immediate: true表示watch初始化时立即执行回调函数getOrderData
watch([() => paginationData.currentPage, () => paginationData.pageSize], getOrderData,{immediate:true})


//标签页（默认第一个）
const activeNameTab = ref('first')
//处理标签页的点击事件
const handleClick = (tab: TabsPaneContext, event: Event) => {
  console.log(tab, event)
}


//异常信息
const exceptionOrder = ref<ErrorInfo[]>([])

//折叠面板显示
const activeNamesCollapse = ref(['1'])
//显示折叠面板边信息
const handleChange = (val: CollapseModelValue) => {
  console.log(val)
}

// 图表数据
const pieData = ref<PieDataItem[]>([])
//
// const pieData = ref([
//   { value: 335, name: '通过工单', itemStyle: { color: '#7EBFDD' } },
//   { value: 310, name: '疑似异常工单', itemStyle: { color: '#FADD66' } },
//   { value: 234, name: '异常工单', itemStyle: { color: '#F67572' } },
// ]);
// const pieData = ref([])

// 图表配置
const option = ref({
  title: {
    text: '工单检测结果',
    left: 'center',
    textStyle: {
      fontSize: 27
    }
  },
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b}: {c} ({d}%)'
  },
  legend: {
    orient: 'vertical',
    left: 'right',
    textStyle: {
      fontSize: 16, 
    }
  },
  series: [
    {
      name: '',
      type: 'pie',
      radius: '70%',
      data: pieData.value,
      label: {
        fontSize: 20
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
});

// 确保图表容器有明确的高度
onMounted(() => {
  const chart = echarts.init(document.querySelector('.chart') as HTMLElement);
  chart.resize({
    width: 600,
    height: 400
  });
});


const handleSelectionChange = (selection: OrderInfo[]) => {
  selectedOrder.value = selection
};

const detectOrder = async () => {
  if (!selectedOrder.value || selectedOrder.value.length === 0) {
    ElMessage.warning('请先选择要检测的工单')
    return
  }

  const orderIds = selectedOrder.value.map(order => order.orderId).join(',')
  
  try {
    const response = await axios({
      method: "get",
      url: `http://127.0.0.1:5555/work_order/infer`,
      params: {
        order_id: orderIds
      }
    })

    const result: OrderDetectResult = response.data
    
    // 更新饼图数据
    pieData.value = [
      { value: result.correct, name: '通过工单', itemStyle: { color: '#7EBFDD' } },
      { value: result.suspect, name: '疑似异常工单', itemStyle: { color: '#FADD66' } },
      { value: result.error, name: '异常工单', itemStyle: { color: '#F67572' } }
    ]
    
    // 更新异常工单列表
    exceptionOrder.value = result.error_info
    
    // 更新图表
    option.value.series[0].data = pieData.value
    
    ElMessage.success('工单检测完成')
  } catch (error) {
    console.error('Error detecting orders:', error)
    ElMessage.error('工单检测失败')
  }
}

</script>

<style>
.example-basic .el-date-editor {
  margin: 8px;
}

.app-container {
  padding: 20px;
}

.SwitchModelCSS {
  display: flex;
  font-size: 15px;
  font-weight: 500;
  padding: 5px;
  justify-content: flex-start;
  align-items: center;
}

.search-wrapper {
  margin-bottom: 20px;
}

.search-wrapper .el-card__body {
  padding-bottom: 15px;
}

.content-center{
  display: flex;
  justify-content: center;
  /* 水平居中 */
  align-items: center;
  /* 垂直居中（如果需要） */
}

.el-collapse-item__header {
  font-size: large;
  color: #F67572;
}

.my-header {
  display: flex;
  gap: 60px;
}

.card-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 16px;
}

.describe_word {
  margin-top: 3px;
  font-size: 20px;
  font-weight: bold;
}

.demo-tabs>.el-tabs__content {
  color: #6b778c;
  font-size: 20px;
}
</style>