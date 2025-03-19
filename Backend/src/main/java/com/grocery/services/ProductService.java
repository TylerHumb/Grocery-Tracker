package com.grocery.services;

import java.util.HashMap;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.grocery.models.Price;
import com.grocery.models.Product;
import com.grocery.repositories.ProductRepository;

@Service
public class ProductService {
    ProductRepository repository;
    @Autowired
    private ProductService(ProductRepository repository){this.repository =repository;}

    public Product getProductByID(String ProductID){
        return repository.getProductByID(ProductID);
    }
    
    public List<Price> getAllPrices(String ProductID){
        return repository.getAllPrices(ProductID);
    }

    public Price getCurrentPrice(String ProductID){
        return repository.getCurrentPrice(ProductID);
    }

    public HashMap<String,Price> Search(String Query){
        return repository.Search(Query);
    }
}
