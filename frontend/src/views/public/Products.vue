<template>
  <div class="products-page">
    <Navbar />
    
    <div class="products-container">
      <h1 class="page-title">产品与服务</h1>
      
      <div class="product-categories">
        <el-tabs v-model="activeTab" class="product-tabs">
          <el-tab-pane label="智能养殖系统" name="system">
            <div class="product-section">
              <h2 class="section-title">智能养殖系统</h2>
              <p class="section-desc">我们的智能养殖系统是一套集环境监控、行为分析、健康管理、饲喂控制于一体的综合解决方案，旨在提高养殖效率、降低成本、保障动物福利。</p>
              
              <div class="product-cards">
                <el-card class="product-card">
                  <div class="product-icon">
                    <el-icon><Monitor /></el-icon>
                  </div>
                  <h3>环境监控系统</h3>
                  <p>实时监测温度、湿度、氨气浓度等环境参数，确保猪舍环境舒适健康。</p>
                  <ul>
                    <li>多点传感器布局，精准监测</li>
                    <li>异常参数自动报警</li>
                    <li>历史数据分析与趋势预测</li>
                    <li>自动化环境调节</li>
                  </ul>
                </el-card>
                
                <el-card class="product-card">
                  <div class="product-icon">
                    <el-icon><VideoCamera /></el-icon>
                  </div>
                  <h3>行为分析系统</h3>
                  <p>通过计算机视觉技术，分析猪只行为模式，及时发现异常。</p>
                  <ul>
                    <li>AI视觉识别技术</li>
                    <li>行为模式分析</li>
                    <li>异常行为预警</li>
                    <li>群体活跃度评估</li>
                  </ul>
                </el-card>
                
                <el-card class="product-card">
                  <div class="product-icon">
                    <el-icon><FirstAidKit /></el-icon>
                  </div>
                  <h3>健康管理系统</h3>
                  <p>通过多维度数据分析，实现猪只健康状况的实时监测与疾病预警。</p>
                  <ul>
                    <li>体温异常监测</li>
                    <li>咳嗽声音识别</li>
                    <li>采食量异常分析</li>
                    <li>疾病风险评估</li>
                  </ul>
                </el-card>
                
                <el-card class="product-card">
                  <div class="product-icon">
                    <el-icon><Dish /></el-icon>
                  </div>
                  <h3>智能饲喂系统</h3>
                  <p>根据猪只生长阶段和健康状况，自动调整饲喂方案，提高饲料利用率。</p>
                  <ul>
                    <li>精准定量投喂</li>
                    <li>个体化饲喂方案</li>
                    <li>饲料消耗分析</li>
                    <li>饲料库存管理</li>
                  </ul>
                </el-card>
              </div>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="硬件设备" name="hardware">
            <div class="product-section">
              <h2 class="section-title">硬件设备</h2>
              <p class="section-desc">我们提供一系列高品质的智能硬件设备，为智能养殖系统提供可靠的数据采集和控制执行能力。</p>
              
              <div class="product-cards">
                <el-card class="product-card">
                  <div class="product-icon">
                    <el-icon><Odometer /></el-icon>
                  </div>
                  <h3>环境传感器</h3>
                  <p>高精度环境参数监测设备，支持温度、湿度、氨气、二氧化碳等多参数监测。</p>
                  <div class="product-price">
                    <span class="price">¥1,200 - ¥3,500</span>
                    <el-button type="primary" size="small">了解详情</el-button>
                  </div>
                </el-card>
                
                <el-card class="product-card">
                  <div class="product-icon">
                    <el-icon><Camera /></el-icon>
                  </div>
                  <h3>智能摄像头</h3>
                  <p>支持红外夜视、防水防尘、高清画质的专业养殖场监控摄像头。</p>
                  <div class="product-price">
                    <span class="price">¥800 - ¥2,500</span>
                    <el-button type="primary" size="small">了解详情</el-button>
                  </div>
                </el-card>
                
                <el-card class="product-card">
                  <div class="product-icon">
                    <el-icon><SetUp /></el-icon>
                  </div>
                  <h3>环境控制设备</h3>
                  <p>智能风机、加热器、喷淋系统等环境调节设备，支持远程控制。</p>
                  <div class="product-price">
                    <span class="price">¥3,000 - ¥15,000</span>
                    <el-button type="primary" size="small">了解详情</el-button>
                  </div>
                </el-card>
                
                <el-card class="product-card">
                  <div class="product-icon">
                    <el-icon><Cpu /></el-icon>
                  </div>
                  <h3>智能控制器</h3>
                  <p>集中管理各类设备的智能控制器，支持多种通信协议和远程升级。</p>
                  <div class="product-price">
                    <span class="price">¥5,000 - ¥12,000</span>
                    <el-button type="primary" size="small">了解详情</el-button>
                  </div>
                </el-card>
              </div>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="技术服务" name="service">
            <div class="product-section">
              <h2 class="section-title">技术服务</h2>
              <p class="section-desc">我们提供全方位的技术服务，从系统规划设计到安装调试，再到运维支持，确保客户获得最佳使用体验。</p>
              
              <div class="service-cards">
                <el-card class="service-card">
                  <h3>系统规划与设计</h3>
                  <p>根据客户需求和场地条件，提供定制化的智能养殖系统规划与设计方案。</p>
                  <ul>
                    <li>需求分析与评估</li>
                    <li>系统架构设计</li>
                    <li>设备布局规划</li>
                    <li>投资回报分析</li>
                  </ul>
                  <el-button type="primary">咨询服务</el-button>
                </el-card>
                
                <el-card class="service-card">
                  <h3>安装与调试</h3>
                  <p>专业团队提供设备安装、系统调试和人员培训服务，确保系统正常运行。</p>
                  <ul>
                    <li>设备安装与布线</li>
                    <li>系统调试与测试</li>
                    <li>操作人员培训</li>
                    <li>系统验收与交付</li>
                  </ul>
                  <el-button type="primary">咨询服务</el-button>
                </el-card>
                
                <el-card class="service-card">
                  <h3>运维与技术支持</h3>
                  <p>提供7×24小时技术支持和定期维护服务，确保系统稳定运行。</p>
                  <ul>
                    <li>远程监控与诊断</li>
                    <li>定期巡检与维护</li>
                    <li>故障排除与修复</li>
                    <li>系统升级与优化</li>
                  </ul>
                  <el-button type="primary">咨询服务</el-button>
                </el-card>
                
                <el-card class="service-card">
                  <h3>数据分析与咨询</h3>
                  <p>基于系统收集的数据，提供专业的养殖管理咨询服务，帮助客户提升养殖效益。</p>
                  <ul>
                    <li>数据分析与报告</li>
                    <li>养殖管理咨询</li>
                    <li>效益提升方案</li>
                    <li>行业趋势分析</li>
                  </ul>
                  <el-button type="primary">咨询服务</el-button>
                </el-card>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
      
      <div class="contact-section">
        <h2>联系我们获取更多产品信息</h2>
        <p>如果您对我们的产品和服务有任何疑问，或者需要定制化解决方案，请随时联系我们。</p>
        <el-button type="primary" size="large">联系销售顾问</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import Navbar from '@/components/layout/Navbar.vue'
import { Monitor, VideoCamera, FirstAidKit, Dish, Odometer, Camera, SetUp, Cpu } from '@element-plus/icons-vue'

export default {
  name: 'ProductsPage',
  components: {
    Navbar,
    Monitor,
    VideoCamera,
    FirstAidKit,
    Dish,
    Odometer,
    Camera,
    SetUp,
    Cpu
  },
  setup() {
    const activeTab = ref('system')
    
    return {
      activeTab
    }
  }
}
</script>

<style scoped>
.products-page {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.products-container {
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

.section-title {
  color: #409EFF;
  margin-bottom: 20px;
  font-size: 24px;
}

.section-desc {
  margin-bottom: 30px;
  color: #606266;
  font-size: 16px;
  line-height: 1.6;
}

.product-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.product-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.product-icon {
  font-size: 40px;
  color: #409EFF;
  margin-bottom: 15px;
  text-align: center;
}

.product-card h3 {
  margin: 0 0 10px;
  color: #303133;
}

.product-card p {
  margin: 0 0 15px;
  color: #606266;
}

.product-card ul {
  margin: 0 0 15px;
  padding-left: 20px;
  color: #606266;
}

.product-card li {
  margin-bottom: 5px;
}

.product-price {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price {
  font-weight: bold;
  color: #F56C6C;
}

.service-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.service-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.service-card h3 {
  margin: 0 0 10px;
  color: #303133;
}

.service-card p {
  margin: 0 0 15px;
  color: #606266;
}

.service-card ul {
  margin: 0 0 20px;
  padding-left: 20px;
  color: #606266;
}

.service-card li {
  margin-bottom: 5px;
}

.service-card .el-button {
  margin-top: auto;
  align-self: flex-start;
}

.contact-section {
  text-align: center;
  margin-top: 60px;
  padding: 40px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.contact-section h2 {
  margin: 0 0 15px;
  color: #303133;
}

.contact-section p {
  margin: 0 0 20px;
  color: #606266;
}

@media (max-width: 768px) {
  .product-cards,
  .service-cards {
    grid-template-columns: 1fr;
  }
}
</style> 