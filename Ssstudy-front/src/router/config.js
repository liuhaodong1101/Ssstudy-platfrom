import TabsView from '@/layouts/tabs/TabsView'
import PageView from '@/layouts/PageView'
// 路由配置
const options = {
  routes: [
    {
      path: '/login',
      name: '登录页',
      component: () => import('@/pages/login')
    },
    {
      path: '/register',
      name: '注册页',
      component: () => import('@/pages/register')
    },
    {
      path: '*',
      name: '404',
      component: () => import('@/pages/exception/404'),
    },
    {
      path: '/403',
      name: '403',
      component: () => import('@/pages/exception/403'),
    },
    {
      path: '/',
      name: '首页',
      component: TabsView,
      redirect: '/login',
      children: [
        {
          path: 'demo',
          name: '首页',
          meta: {
            icon: 'file-ppt',
            noCache: true,
            meta: [
              { name: 'Cache-Control', content: 'no-cache, no-store, must-revalidate' },
            ],
          },
          component: () => import('@/pages/demo')
        },
        {
          path: 'stuInfo',
          name: '个人信息',
          meta: {
            icon: 'file-ppt'
          },
          component: () => import('@/pages/stuInfo')
        },
        {
          path: 'course',
          name: '选课',
          meta: {
            icon: 'form'
          },
          component: PageView,
          children: [
            {
              path: 'showCourse',
              name: '查看选课列表',
              component: () => import('@/pages/showCourse'),
            },
            {
              path: 'download/:id',
              name: '文件下载页',
              component: () => import('@/pages/download'),
            }
          ]
        },
        {
          path: 'communitys',
          name: '社区',
          meta: {
            icon: 'form'
          },
          component: PageView,
          children: [
            {
              path: 'communityList',  // 使用动态参数:id表示社区ID
              name: '查看社区列表',
              component: () => import('../pages/communityList'),
            },
            // 新增社区详情路由
            {
              path: 'commnuity/:id',
              name: '社区详情',
              component: () => import('../pages/showCommunity'),
            },
            //新增查看点赞的帖子
            {
              path: 'likePost',
              name: '您点赞的帖子',
              component: () => import('../pages/showMyLike'),
            },
            //新增查看点赞的帖子
            {
              path: 'yourPost',
              name: '您的帖子',
              component: () => import('../pages/showMyPost'),
            }
          ]
        },

        {
          name: '验权页面',
          path: 'auth/demo',
          meta: {
            icon: 'file-ppt',
            authority: {
              permission: 'form',
              role: 'manager'
            },
            component: () => import('@/pages/demo')
          }
        }
      ]
    }
  ]
}

export default options
