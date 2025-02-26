package com.grocery.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

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
    
}
