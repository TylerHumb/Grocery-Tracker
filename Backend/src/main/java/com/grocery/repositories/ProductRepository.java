package com.grocery.repositories;

import javax.sql.DataSource;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

@Repository
public class ProductRepository {
    DataSource source;
    @Autowired
    public ProductRepository(DataSource source){this.source = source;}
}