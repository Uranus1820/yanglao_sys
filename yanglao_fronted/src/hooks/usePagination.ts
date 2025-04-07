import { reactive } from "vue"
interface IDefaultPaginationData {
    total: number
    currentPage: number
    pageSize: number
    layout: string
  }
  
  interface IPaginationData {
    total?: number
    currentPage?: number
    pageSizes?: number[]
    pageSize?: number
    layout?: string
  }
  
  /** 默认的分页参数 */
  const defaultPaginationData: IDefaultPaginationData = {
    total: 0,
    currentPage: 1,
    pageSize: 10, //每页是个数据
    layout: "total, prev, pager, next"
  }
  
  export function usePagination(_paginationData: IPaginationData = {}) {
    /** 合并分页参数 */
    const paginationData = reactive(Object.assign({ ...defaultPaginationData }, _paginationData))
  
    /** 改变当前页码 */
    const handleCurrentChange = (value: number) => {
      paginationData.currentPage = value
    }
  
    /** 改变页面大小 */
    const handleSizeChange = (value: number) => {
      paginationData.pageSize = value
    }
  
    return { paginationData, handleCurrentChange, handleSizeChange }
  }