<template>
  <div class="news-page">
    <Navbar />
    
    <div class="news-container">
      <h1 class="page-title">新闻动态</h1>
      
      <div class="news-filter">
        <el-radio-group v-model="activeCategory" size="large">
          <el-radio-button label="all">全部</el-radio-button>
          <el-radio-button label="company">公司动态</el-radio-button>
          <el-radio-button label="industry">行业资讯</el-radio-button>
          <el-radio-button label="technology">技术前沿</el-radio-button>
        </el-radio-group>
        
        <el-input
          v-model="searchKeyword"
          placeholder="搜索新闻"
          class="search-input"
          clearable
          prefix-icon="Search"
        />
      </div>
      
      <div class="news-list">
        <el-card v-for="(news, index) in filteredNews" :key="index" class="news-card">
          <div class="news-content">
            <div class="news-image">
              <el-image :src="news.image" fit="cover" />
            </div>
            <div class="news-info">
              <div class="news-category">
                <el-tag :type="getCategoryType(news.category)">{{ getCategoryName(news.category) }}</el-tag>
                <span class="news-date">{{ news.date }}</span>
              </div>
              <h2 class="news-title">{{ news.title }}</h2>
              <p class="news-summary">{{ news.summary }}</p>
              <el-button type="primary" text>阅读更多</el-button>
            </div>
          </div>
        </el-card>
        
        <el-empty v-if="filteredNews.length === 0" description="暂无相关新闻" />
      </div>
      
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="filteredNews.length"
          layout="prev, pager, next"
          background
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import Navbar from '@/components/layout/Navbar.vue'
import { Search } from '@element-plus/icons-vue'

export default {
  name: 'NewsPage',
  components: {
    Navbar,
    Search
  },
  setup() {
    const activeCategory = ref('all')
    const searchKeyword = ref('')
    const currentPage = ref(1)
    const pageSize = ref(5)
    
    const newsList = ref([
      {
        title: '泓泰生物科技荣获"2023年度智能养殖领军企业"称号',
        summary: '近日，在第十届中国畜牧业博览会上，泓泰生物科技凭借在智能养殖领域的突出贡献，荣获"2023年度智能养殖领军企业"称号。',
        image: require('@/assets/news1.jpg'),
        category: 'company',
        date: '2023-12-15'
      },
      {
        title: '我公司智能养猪系统在山东某大型养殖基地成功落地',
        summary: '近日，我公司自主研发的智能养猪系统在山东某大型养殖基地成功落地，该系统通过环境监测、行为分析等功能，显著提高了养殖效率。',
        image: require('@/assets/news2.jpg'),
        category: 'company',
        date: '2023-11-28'
      },
      {
        title: '2023年中国智能养殖行业发展趋势分析',
        summary: '随着人工智能、物联网等技术的快速发展，智能养殖行业正迎来前所未有的发展机遇。本文分析了2023年中国智能养殖行业的主要发展趋势。',
        image: require('@/assets/news3.jpg'),
        category: 'industry',
        date: '2023-10-15'
      },
      {
        title: '人工智能在畜牧业中的应用与前景',
        summary: '人工智能技术在畜牧业中的应用正日益广泛，从环境监控到动物行为分析，再到疾病预警，AI技术正在重塑传统养殖业。',
        image: require('@/assets/news1.jpg'),
        category: 'technology',
        date: '2023-09-20'
      },
      {
        title: '我公司与农业大学达成战略合作',
        summary: '近日，我公司与中国农业大学签署战略合作协议，双方将在智能养殖技术研发、人才培养等方面展开深入合作。',
        image: require('@/assets/news2.jpg'),
        category: 'company',
        date: '2023-08-10'
      },
      {
        title: '智能养殖如何助力乡村振兴',
        summary: '智能养殖技术的推广应用，不仅提高了养殖效率，降低了成本，还为乡村振兴战略提供了新的发展路径。',
        image: require('@/assets/news3.jpg'),
        category: 'industry',
        date: '2023-07-25'
      },
      {
        title: '物联网技术在养猪场中的应用案例分析',
        summary: '本文通过多个实际案例，详细分析了物联网技术在现代化养猪场中的应用方式及其带来的效益提升。',
        image: require('@/assets/news1.jpg'),
        category: 'technology',
        date: '2023-06-18'
      }
    ])
    
    const filteredNews = computed(() => {
      let result = newsList.value
      
      // 按分类筛选
      if (activeCategory.value !== 'all') {
        result = result.filter(item => item.category === activeCategory.value)
      }
      
      // 按关键词搜索
      if (searchKeyword.value) {
        const keyword = searchKeyword.value.toLowerCase()
        result = result.filter(item => 
          item.title.toLowerCase().includes(keyword) || 
          item.summary.toLowerCase().includes(keyword)
        )
      }
      
      return result
    })
    
    const getCategoryName = (category) => {
      const categoryMap = {
        'company': '公司动态',
        'industry': '行业资讯',
        'technology': '技术前沿'
      }
      return categoryMap[category] || category
    }
    
    const getCategoryType = (category) => {
      const typeMap = {
        'company': 'success',
        'industry': 'info',
        'technology': 'warning'
      }
      return typeMap[category] || ''
    }
    
    return {
      activeCategory,
      searchKeyword,
      currentPage,
      pageSize,
      filteredNews,
      getCategoryName,
      getCategoryType
    }
  }
}
</script>

<style scoped>
.news-page {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.news-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.page-title {
  text-align: center;
  margin-bottom: 40px;
  color: #303133;
  font-size: 36px;
}

.news-filter {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.search-input {
  width: 300px;
}

.news-list {
  margin-bottom: 30px;
}

.news-card {
  margin-bottom: 20px;
}

.news-content {
  display: flex;
  gap: 20px;
}

.news-image {
  flex: 0 0 200px;
  height: 150px;
  overflow: hidden;
  border-radius: 4px;
}

.news-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.news-category {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.news-date {
  margin-left: 10px;
  color: #909399;
  font-size: 14px;
}

.news-title {
  margin: 0 0 10px;
  font-size: 18px;
  color: #303133;
}

.news-summary {
  margin: 0 0 15px;
  color: #606266;
  flex: 1;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

@media (max-width: 768px) {
  .news-filter {
    flex-direction: column;
    gap: 15px;
  }
  
  .search-input {
    width: 100%;
  }
  
  .news-content {
    flex-direction: column;
  }
  
  .news-image {
    flex: 0 0 auto;
    width: 100%;
    height: 200px;
  }
}
</style> 