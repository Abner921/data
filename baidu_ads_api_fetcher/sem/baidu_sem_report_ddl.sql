use etl;
drop table t_baidu_sem_report;
drop table t_baidu_sem_account;
drop table t_baidu_sem_campaign;
drop table t_baidu_sem_adgroup;
drop table t_baidu_sem_keyword;
drop table t_baidu_sem_creative;
drop table t_baidu_sem_region;

create table t_baidu_sem_report(
  id             int(11) NOT NULL AUTO_INCREMENT,
  create_date    timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  date           varchar(20) DEFAULT NULL,
  accountId      varchar(20) DEFAULT NULL,
  campaignId     varchar(20) DEFAULT NULL,
  adgroupId      varchar(20) DEFAULT NULL,

  keywordId      varchar(20) DEFAULT NULL,
  wordId         varchar(20) DEFAULT NULL,

  creativeId     varchar(20) DEFAULT NULL,
  regionId       varchar(20) DEFAULT NULL,

  impression     varchar(20) DEFAULT NULL,
  click          varchar(20) DEFAULT NULL,
  cost           varchar(20) DEFAULT NULL,
  cpc            varchar(20) DEFAULT NULL,
  ctr            varchar(20) DEFAULT NULL,
  cpm            varchar(20) DEFAULT NULL,

  device         varchar(10) DEFAULT NULL,
  unitOfTime     varchar(10) DEFAULT NULL,
  report_typ     varchar(20) DEFAULT NULL,

  PRIMARY KEY (`id`)
)ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

create table t_baidu_sem_account(
  id             int(11) NOT NULL AUTO_INCREMENT,
  accountId      varchar(20) DEFAULT NULL,
  account        varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
)ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


create table t_baidu_sem_campaign(
  id             int(11) NOT NULL AUTO_INCREMENT,
  campaignId     varchar(20) DEFAULT NULL,
  campaignName   varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
)ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

create table t_baidu_sem_adgroup(
  id             int(11) NOT NULL AUTO_INCREMENT,
  adgroupId      varchar(20) DEFAULT NULL,
  adgroupName    varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)

)ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

create table t_baidu_sem_keyword(
  id             int(11) NOT NULL AUTO_INCREMENT,
  keywordId      varchar(20) DEFAULT NULL,
  wordId         varchar(20) DEFAULT NULL,
  keyword        varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
)ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

create table t_baidu_sem_creative(
  id             int(11) NOT NULL AUTO_INCREMENT,
  creativeId     varchar(20) DEFAULT NULL,
  title          varchar(20) DEFAULT NULL,
  description1   varchar(20) DEFAULT NULL,
  description2   varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)

)ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

create table t_baidu_sem_region(
  id             int(11) NOT NULL AUTO_INCREMENT,
  regionId       varchar(20) DEFAULT NULL,
  region         varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
)ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

create or replace view v_baidu_sem_report as
   select rpt.create_date,
          rpt.date,
          rpt.unitOfTime,
          rpt.report_typ,
          case rpt.unitOfTime
           when '1' then str_to_date(rpt.date,'%Y')
           when '3' then str_to_date(rpt.date,'%Y-%m')
           when '5' then str_to_date(rpt.date,'%Y-%m-%d')
           when '7' then str_to_date(rpt.date,'%Y-%m-%d %H')
           else rpt.date END date2,
          case  when instr(adg.adgroupName,'品牌') then '品牌'
           when instr(adg.adgroupName,'楼盘') then '品牌'
           when instr(adg.adgroupName,'竞品') then '竞品'
           when instr(adg.adgroupName,'区域') then '区域'
           else '通用' END fenlei,
          cast(rpt.impression as decimal(10,2) ) impression,
          cast(rpt.click as decimal(10,2) ) click,
          cast(rpt.cost as decimal(10,2) ) cost,
          acc.account,
          cam.campaignName,
          adg.adgroupName,
          ky.keyword,
          cre.title,
          reg.region,
          SUBSTRING(substring_index(cam.campaignName,'-',2),
                    (char_length(substring_index(cam.campaignName,'-',1))+2))  loupan
     from t_baidu_sem_report rpt
     left join t_baidu_sem_account acc
       on rpt.accountId = acc.accountId
     left join t_baidu_sem_campaign cam
       on rpt.campaignId = cam.campaignId
     left join t_baidu_sem_adgroup adg
       on rpt.adgroupId = adg.adgroupId
     left join t_baidu_sem_keyword ky
       on rpt.keywordId = ky.keywordId
     left join t_baidu_sem_creative cre
       on rpt.creativeId = cre.creativeId
     left join t_baidu_sem_region reg
       on rpt.regionId = reg.regionId
;