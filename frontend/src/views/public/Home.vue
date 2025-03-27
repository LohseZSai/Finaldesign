<template>
  <div class="home-page">
    <!-- 导航栏 -->
    <Navbar />
    
    <!-- 全屏轮播图 -->
    <section class="hero-section">
      <el-carousel height="600px" :interval="5000" arrow="always" indicator-position="none">
        <el-carousel-item v-for="(slide, index) in heroSlides" :key="index">
          <div class="slide-content" :style="{ backgroundImage: `url(${slide.image})` }">
            <div class="slide-overlay"></div>
            <div class="slide-text">
              <h1>{{ slide.title }}</h1>
              <p>{{ slide.description }}</p>
              <el-button type="primary" size="large" @click="navigateTo(slide.buttonLink)">
                {{ slide.buttonText }}
              </el-button>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </section>
    
    <!-- 企业优势 -->
    <section class="advantages-section">
      <div class="section-container">
        <h2 class="section-title">我们的优势</h2>
        <p class="section-subtitle">智能化养殖解决方案，提升生产效率，降低运营成本</p>
        
        <div class="advantages-grid">
          <div class="advantage-item" v-for="(advantage, index) in advantages" :key="index">
            <div class="advantage-icon">
              <el-icon :size="50"><component :is="advantage.icon" /></el-icon>
            </div>
            <h3>{{ advantage.title }}</h3>
            <p>{{ advantage.description }}</p>
          </div>
        </div>
      </div>
    </section>
    
    <!-- 数据统计 -->
    <section class="stats-section">
      <div class="section-container">
        <div class="stats-grid">
          <div class="stat-item" v-for="(stat, index) in statistics" :key="index">
            <div class="stat-number">{{ stat.number }}</div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- 新闻动态 -->
    <section class="news-section">
      <div class="section-container">
        <h2 class="section-title">新闻动态</h2>
        <p class="section-subtitle">了解我们的最新动态和行业资讯</p>
        
        <div class="news-grid">
          <el-card class="news-card" v-for="(news, index) in latestNews" :key="index" shadow="hover">
            <img :src="news.image" class="news-image" />
            <div class="news-date">{{ news.date }}</div>
            <h3 class="news-title">{{ news.title }}</h3>
            <p class="news-summary">{{ news.summary }}</p>
            <el-button type="text" @click="navigateTo('/news')">阅读更多</el-button>
          </el-card>
        </div>
        
        <div class="view-more">
          <el-button type="primary" @click="navigateTo('/news')">查看更多新闻</el-button>
        </div>
      </div>
    </section>
    
    <!-- 合作伙伴 -->
    <section class="partners-section">
      <div class="section-container">
        <h2 class="section-title">合作伙伴</h2>
        <p class="section-subtitle">与行业领先企业携手共进</p>
        
        <div class="partners-grid">
          <div class="partner-item" v-for="(partner, index) in partners" :key="index">
            <img :src="partner.logo" :alt="partner.name" class="partner-logo" />
          </div>
        </div>
      </div>
    </section>
    
    <!-- 联系我们 -->
    <section class="contact-section">
      <div class="section-container">
        <div class="contact-grid">
          <div class="contact-info">
            <h2>联系我们</h2>
            <p>如果您对我们的产品和服务有任何疑问，或者需要定制化解决方案，请随时联系我们。</p>
            <div class="contact-item">
              <el-icon><Location /></el-icon>
              <span>杭州市西湖区文三路478号智慧产业园A座15楼</span>
            </div>
            <div class="contact-item">
              <el-icon><Phone /></el-icon>
              <span>0571-88888888</span>
            </div>
            <div class="contact-item">
              <el-icon><Message /></el-icon>
              <span>contact@hongtai-tech.com</span>
            </div>
          </div>
          
          <div class="contact-form">
            <h3>发送消息</h3>
            <el-form :model="contactForm" label-position="top">
              <el-form-item label="姓名">
                <el-input v-model="contactForm.name" placeholder="请输入您的姓名" />
              </el-form-item>
              <el-form-item label="电话">
                <el-input v-model="contactForm.phone" placeholder="请输入您的电话" />
              </el-form-item>
              <el-form-item label="邮箱">
                <el-input v-model="contactForm.email" placeholder="请输入您的邮箱" />
              </el-form-item>
              <el-form-item label="留言">
                <el-input v-model="contactForm.message" type="textarea" rows="4" placeholder="请输入您的留言" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="submitContactForm">提交</el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
      </div>
    </section>
    
    <!-- 页脚 -->
    <footer class="footer">
      <div class="section-container">
        <div class="footer-grid">
          <div class="footer-column">
            <img src="@/assets/logo.svg" alt="泓泰生物科技" class="footer-logo" />
            <p>泓泰生物科技有限公司是一家专注于智能养殖技术研发与应用的高新技术企业。</p>
          </div>
          
          <div class="footer-column">
            <h3>快速链接</h3>
            <ul>
              <li><a href="/">首页</a></li>
              <li><a href="/products">产品服务</a></li>
              <li><a href="/news">新闻动态</a></li>
              <li><a href="/about">关于我们</a></li>
            </ul>
          </div>
          
          <div class="footer-column">
            <h3>联系方式</h3>
            <p>杭州市西湖区文三路478号智慧产业园A座15楼</p>
            <p>电话: 0571-88888888</p>
            <p>邮箱: contact@hongtai-tech.com</p>
          </div>
        </div>
        
        <div class="footer-bottom">
          <p>&copy; 2025 泓泰生物科技有限公司. 保留所有权利.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '@/components/layout/Navbar.vue'
import { ElMessage } from 'element-plus'
import { 
  Monitor, 
  DataLine, 
  Cpu, 
  Connection, 
  Location, 
  Phone, 
  Message 
} from '@element-plus/icons-vue'

export default {
  name: 'HomePage',
  components: {
    Navbar,
    Monitor,
    DataLine,
    Cpu,
    Connection,
    Location,
    Phone,
    Message
  },
  
  setup() {
    const router = useRouter()
    
    // 轮播图数据
    const heroSlides = ref([
      {
        title: '智能养殖解决方案',
        description: '利用人工智能和物联网技术，提升养殖效率，降低成本，保障动物福利',
        buttonText: '了解更多',
        buttonLink: '/products',
        image: require('@/assets/hero1.jpg')
      },
      {
        title: '数据驱动的精准养殖',
        description: '通过实时数据监测和分析，实现精准化、智能化养殖管理',
        buttonText: '查看产品',
        buttonLink: '/products',
        image: require('@/assets/hero2.jpg')
      },
      {
        title: '全方位技术支持',
        description: '提供从系统规划到运维支持的全方位技术服务，确保您的养殖业务顺利运行',
        buttonText: '联系我们',
        buttonLink: '/about',
        image: require('@/assets/hero3.jpg')
      }
    ])
    
    // 企业优势数据
    const advantages = ref([
      {
        icon: 'Monitor',
        title: '实时环境监控',
        description: '24小时监测温度、湿度、氨气等环境参数，确保最佳生长环境'
      },
      {
        icon: 'DataLine',
        title: '数据分析预警',
        description: '基于大数据分析，提前预警潜在风险，减少损失'
      },
      {
        icon: 'Cpu',
        title: '智能设备控制',
        description: '自动化控制环境调节设备，减少人工干预，提高效率'
      },
      {
        icon: 'Connection',
        title: '系统集成方案',
        description: '提供一体化解决方案，实现养殖全流程数字化管理'
      }
    ])
    
    // 数据统计
    const statistics = ref([
      {
        number: '200+',
        label: '合作客户'
      },
      {
        number: '50+',
        label: '服务项目'
      },
      {
        number: '15+',
        label: '行业经验'
      },
      {
        number: '98%',
        label: '客户满意度'
      }
    ])
    
    // 最新新闻
    const latestNews = ref([
      {
        title: '泓泰生物科技荣获"2023年度智能养殖领军企业"称号',
        summary: '近日，在第十届中国畜牧业博览会上，泓泰生物科技凭借在智能养殖领域的突出贡献，荣获"2023年度智能养殖领军企业"称号。',
        date: '2023-12-15',
        image: require('@/assets/news1.jpg')
      },
      {
        title: '我公司智能养猪系统在山东某大型养殖基地成功落地',
        summary: '近日，我公司自主研发的智能养猪系统在山东某大型养殖基地成功落地，该系统通过环境监测、行为分析等功能，显著提高了养殖效率。',
        date: '2023-11-28',
        image: require('@/assets/news2.jpg')
      },
      {
        title: '2023年中国智能养殖行业发展趋势分析',
        summary: '随着人工智能、物联网等技术的快速发展，智能养殖行业正迎来前所未有的发展机遇。本文分析了2023年中国智能养殖行业的主要发展趋势。',
        date: '2023-10-15',
        image: require('@/assets/news3.jpg')
      }
    ])
    
    // 合作伙伴
    const partners = ref([
      {
        name: '合作伙伴1',
        logo: require('@/assets/partner1.png')
      },
      {
        name: '合作伙伴2',
        logo: require('@/assets/partner2.png')
      },
      {
        name: '合作伙伴3',
        logo: require('@/assets/partner3.png')
      },
      {
        name: '合作伙伴4',
        logo: require('@/assets/partner4.png')
      },
      {
        name: '合作伙伴5',
        logo: require('@/assets/partner5.png')
      }
    ])
    
    // 联系表单
    const contactForm = reactive({
      name: '',
      phone: '',
      email: '',
      message: ''
    })
    
    // 导航方法
    const navigateTo = (path) => {
      router.push(path)
    }
    
    const submitContactForm = () => {
      // 这里可以添加表单验证逻辑
      ElMessage.success('您的留言已提交，我们将尽快与您联系！')
      // 重置表单
      contactForm.name = ''
      contactForm.phone = ''
      contactForm.email = ''
      contactForm.message = ''
    }
    
    return {
      heroSlides,
      advantages,
      statistics,
      latestNews,
      partners,
      contactForm,
      navigateTo,
      submitContactForm
    }
  }
}
</script>

<style scoped>
.home-page {
  min-height: 100vh;
}

/* 通用部分样式 */
.section-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 80px 20px;
}

.section-title {
  text-align: center;
  font-size: 36px;
  color: #303133;
  margin-bottom: 20px;
}

.section-subtitle {
  text-align: center;
  font-size: 18px;
  color: #606266;
  margin-bottom: 50px;
}

/* 轮播图部分样式 */
.hero-section {
  position: relative;
}

.slide-content {
  height: 100%;
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.slide-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.slide-text {
  position: relative;
  z-index: 1;
  text-align: center;
  color: white;
  max-width: 800px;
  padding: 0 20px;
}

.slide-text h1 {
  font-size: 48px;
  margin-bottom: 20px;
}

.slide-text p {
  font-size: 20px;
  margin-bottom: 30px;
}

/* 企业优势样式 */
.advantages-section {
  background-color: #f5f7fa;
}

.advantages-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 30px;
}

.advantage-item {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s;
}

.advantage-item:hover {
  transform: translateY(-10px);
}

.advantage-icon {
  color: #409EFF;
  margin-bottom: 20px;
}

.advantage-item h3 {
  font-size: 20px;
  color: #303133;
  margin-bottom: 15px;
}

.advantage-item p {
  color: #606266;
  line-height: 1.6;
}

/* 数据统计样式 */
.stats-section {
  background-color: #409EFF;
  color: white;
}

.stats-section .section-container {
  padding: 60px 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 30px;
  text-align: center;
}

.stat-number {
  font-size: 48px;
  font-weight: bold;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 18px;
}

/* 新闻动态样式 */
.news-section {
  background-color: white;
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 30px;
  margin-bottom: 40px;
}

.news-card {
  height: 100%;
  transition: transform 0.3s;
}

.news-card:hover {
  transform: translateY(-5px);
}

.news-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 15px;
}

.news-date {
  color: #909399;
  font-size: 14px;
  margin-bottom: 10px;
}

.news-title {
  font-size: 18px;
  color: #303133;
  margin-bottom: 10px;
  line-height: 1.4;
}

.news-summary {
  color: #606266;
  margin-bottom: 15px;
  line-height: 1.6;
}

.view-more {
  text-align: center;
}

/* 合作伙伴样式 */
.partners-section {
  background-color: #f5f7fa;
}

.partners-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 30px;
  align-items: center;
}

.partner-item {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  text-align: center;
}

.partner-logo {
  max-width: 100%;
  height: 80px;
  object-fit: contain;
}

/* 联系我们样式 */
.contact-section {
  background-color: white;
}

.contact-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 50px;
}

.contact-info h2 {
  font-size: 28px;
  color: #303133;
  margin-bottom: 20px;
}

.contact-info p {
  color: #606266;
  margin-bottom: 30px;
  line-height: 1.6;
}

.contact-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  color: #606266;
}

.contact-item .el-icon {
  margin-right: 10px;
  color: #409EFF;
}

.contact-form h3 {
  font-size: 24px;
  color: #303133;
  margin-bottom: 20px;
}

/* 页脚样式 */
.footer {
  background-color: #001529;
  color: white;
}

.footer .section-container {
  padding: 60px 20px 30px;
}

.footer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 40px;
  margin-bottom: 40px;
}

.footer-logo {
  height: 40px;
  margin-bottom: 20px;
}

.footer-column p {
  color: #a6a9ad;
  line-height: 1.6;
}

.footer-column h3 {
  font-size: 18px;
  margin-bottom: 20px;
  position: relative;
  padding-bottom: 10px;
}

.footer-column h3::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 50px;
  height: 2px;
  background-color: #409EFF;
}

.footer-column ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-column ul li {
  margin-bottom: 10px;
}

.footer-column ul li a {
  color: #a6a9ad;
  text-decoration: none;
  transition: color 0.3s;
}

.footer-column ul li a:hover {
  color: #409EFF;
}

.footer-bottom {
  text-align: center;
  padding-top: 30px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-bottom p {
  color: #a6a9ad;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .slide-text h1 {
    font-size: 32px;
  }
  
  .slide-text p {
    font-size: 16px;
  }
  
  .contact-grid {
    grid-template-columns: 1fr;
  }
  
  .section-container {
    padding: 60px 20px;
  }
}
</style> 