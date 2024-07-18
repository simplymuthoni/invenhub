import React, { useState, useEffect } from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AdminLogin from './components/AdminLogin';
import AdminRegister from './components/AdminRegister';
import Register from './components/Register';
import LoginPage from './components/LoginPage';
import InventoryList from './components/InventoryList';
import AddItem from './components/AddItem';
import EditItem from './components/EditItem';
import ItemForm from './components/ItemForm';
import ItemList from './components/ItemList';
import axios from 'axios';
import Login from './components/Login';
import Logout from './components/Logout';
import ChangePassword from './components/ChangePassword';
import ResetPassword from './components/ResetPassword';

const App = () => {
  const [items, setItems] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/items')
      .then(response => setItems(response.data))
      .catch(error => console.error('Error fetching items:', error));
  }, []);

  const addItem = (item) => {
    axios.post('http://localhost:5000/items', item)
      .then(response => setItems([...items, response.data]))
      .catch(error => console.error('Error adding item:', error));
  };

  const deleteItem = (itemId) => {
    axios.delete(`http://localhost:5000/items/${itemId}`)
      .then(() => setItems(items.filter(item => item.id !== itemId)))
      .catch(error => console.error('Error deleting item:', error));
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/admin/login" element={<AdminLogin />} />
        <Route path="/admin/register" element={<AdminRegister />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/change_password" element={<ChangePassword />} />
        <Route path="/reset_password" element={<ResetPassword />} />
        <Route path="/inventory" element={
          <div>
            <h1>Clothing Inventory</h1>
            <ItemForm onAdd={addItem} />
            <ItemList items={items} onDelete={deleteItem} />
          </div>
        } />
        <Route path="/add-item" element={<AddItem />} />
        <Route path="/items/:id/edit" element={<EditItem />} />
      </Routes>
    </Router>
  );
};

const RegisterPage = () => {
  return (
    <div className="App">
      <header className="App-header">
        <h1>User Registration</h1>
        <Register />
      </header>
    </div>
  );
};

export default App;
