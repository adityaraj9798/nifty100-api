from django.db import models

class DimCompany(models.Model):
    symbol = models.TextField(db_column='mkt_fintech_—_nifty_100__|__companies__|__92_records', primary_key=True)
    logo_url = models.TextField(db_column='unnamed:_1', blank=True, null=True)
    company_name = models.TextField(db_column='unnamed:_2', blank=True, null=True)
    chart_link = models.TextField(db_column='unnamed:_3', blank=True, null=True)
    description = models.TextField(db_column='unnamed:_4', blank=True, null=True)
    website = models.TextField(db_column='unnamed:_5', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_company'

class FactProfitLoss(models.Model):
    symbol = models.TextField(db_column='year_label', primary_key=True)
    # Changed from 'year' to 'fiscal_year'
    year = models.IntegerField(db_column='fiscal_year', blank=True, null=True) 
    revenue = models.FloatField(db_column='unnamed:_3', blank=True, null=True) 
    net_profit = models.FloatField(db_column='unnamed:_12', blank=True, null=True) 
    eps = models.FloatField(db_column='unnamed:_13', blank=True, null=True) 

    class Meta:
        managed = False
        db_table = 'fact_profit_loss'

class FactBalanceSheet(models.Model):
    symbol = models.TextField(db_column='year_label', primary_key=True)
    # Changed from 'year' to 'fiscal_year'
    year = models.IntegerField(db_column='fiscal_year', blank=True, null=True)
    total_assets = models.FloatField(db_column='unnamed:_10', blank=True, null=True)
    total_liabilities = models.FloatField(db_column='unnamed:_5', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fact_balance_sheet'