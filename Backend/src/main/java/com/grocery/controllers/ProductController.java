package com.grocery.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.grocery.models.Product;
import com.grocery.services.ProductService;


@RestController
@RequestMapping(value = "products")
public class ProductController {
    private ProductService service;

    @Autowired
    public ProductController(ProductService service){this.service = service;}

    @GetMapping("/{productid}")
    public Product getProductByID(@PathVariable String productid){
        return service.getProductByID(productid);
    }

}
