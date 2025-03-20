import './App.css';
import HomePage from './HomePage'
import Search from './Search'
import ProductPage from './ProductPage'

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <div className="App">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/search/:query" element={<Search />} />
          <Route path="/product/:productid" element={<ProductPage />} />
        </Routes>
    </div>
  );
}

export default function AppWrapper() {
  return (
    <Router>
      <App />
    </Router>
  );
}
