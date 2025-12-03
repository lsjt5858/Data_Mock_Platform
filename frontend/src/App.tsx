import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import { DatabaseOutlined, ThunderboltOutlined } from '@ant-design/icons';
import { TemplateEditor } from './pages/TemplateEditor';
import { DataGenerate } from './pages/DataGenerate';
import './App.css';

const { Header, Content } = Layout;

function App() {
  return (
    <BrowserRouter>
      <Layout style={{ minHeight: '100vh' }}>
        <Header style={{ background: '#fff', padding: '0 24px', borderBottom: '1px solid #f0f0f0' }}>
          <div style={{ display: 'flex', alignItems: 'center', height: 64 }}>
            <div style={{ fontSize: 20, fontWeight: 'bold', marginRight: 32 }}>
              数据生成平台
            </div>
            <Menu mode="horizontal" defaultSelectedKeys={['1']} style={{ flex: 1, border: 'none' }}>
              <Menu.Item key="1" icon={<DatabaseOutlined />}>
                <Link to="/">模板编辑</Link>
              </Menu.Item>
              <Menu.Item key="2" icon={<ThunderboltOutlined />}>
                <Link to="/generate">数据生成</Link>
              </Menu.Item>
            </Menu>
          </div>
        </Header>
        <Content style={{ background: '#f0f2f5' }}>
          <Routes>
            <Route path="/" element={<TemplateEditor />} />
            <Route path="/generate" element={<DataGenerate />} />
          </Routes>
        </Content>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
