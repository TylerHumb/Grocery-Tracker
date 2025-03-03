package com.grocery.controllers;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.grocery.models.Price;
import com.grocery.models.Product;
import com.grocery.services.ProductService;


@RestController
@RequestMapping(value = "products")
public class ProductController {
    private ProductService service;

    @Autowired
    public ProductController(ProductService service){this.service = service;}

    @GetMapping("/{ProductID}")
    public Product getProductByID(@PathVariable String ProductID){
        return service.getProductByID(ProductID);
    }

    @GetMapping("/allprice/{ProductID}")
    public List<Price> getAllPrices(@PathVariable String ProductID){
        return service.getAllPrices(ProductID);
    }

    @GetMapping("/lastprice/{ProductID}")
    public Price getCurrentPrice(@PathVariable String ProductID){
        return service.getCurrentPrice(ProductID);
    }

}
