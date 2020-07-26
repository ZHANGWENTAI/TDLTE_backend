IF EXISTS(SELECT * FROM sysobjects WHERE NAME='chk_enodeb_vendor')
	ALTER TABLE enodeb DROP CONSTRAINT chk_enodeb_vendor;
IF EXISTS(SELECT * FROM sysobjects WHERE NAME='chk_enodeb_style')
	ALTER TABLE enodeb DROP CONSTRAINT chk_enodeb_style;
IF EXISTS(SELECT * FROM sysobjects WHERE NAME='chk_cell_pci')
	ALTER TABLE cell DROP CONSTRAINT chk_cell_pci;
IF EXISTS(SELECT * FROM sysobjects WHERE NAME='chk_cell_earfcn')
	ALTER TABLE cell DROP CONSTRAINT chk_cell_earfcn;
IF EXISTS(SELECT * FROM sysobjects WHERE NAME='chk_cell_pss')
	ALTER TABLE cell DROP CONSTRAINT chk_cell_pss;
IF EXISTS(SELECT * FROM sysobjects WHERE NAME='chk_cell_sss')
	ALTER TABLE cell DROP CONSTRAINT chk_cell_sss;
IF EXISTS(SELECT * FROM sysobjects WHERE NAME='chk_cell_totletilt')
	ALTER TABLE cell DROP CONSTRAINT chk_cell_totletilt;
IF EXISTS(SELECT * FROM sysobjects WHERE NAME='chk_optcell_earfcn')
	ALTER TABLE optcell DROP CONSTRAINT chk_optcell_earfcn;
IF EXISTS(SELECT * FROM sysobjects WHERE NAME='chk_optcell_celltype')
	ALTER TABLE optcell DROP CONSTRAINT chk_optcell_celltype;
IF EXISTS(SELECT * FROM sysobjects WHERE NAME='chk_pciassignment_earfcn')
	ALTER TABLE pciassignment DROP CONSTRAINT chk_pciassignment_earfcn;
IF EXISTS(SELECT * FROM sysobjects WHERE NAME='chk_pciassignment_style')
	ALTER TABLE pciassignment DROP CONSTRAINT chk_pciassignment_style;
IF EXISTS(SELECT * FROM sysobjects WHERE NAME='fk_cell_enodeb_1')
	ALTER TABLE cell DROP CONSTRAINT fk_cell_enodeb_1;

IF EXISTS(SELECT TOP 1 * FROM sysObjects WHERE Id=OBJECT_ID(N'enodeb') and xtype='U')
	DROP TABLE enodeb;
IF EXISTS(SELECT TOP 1 * FROM sysObjects WHERE Id=OBJECT_ID(N'cell') and xtype='U')
	DROP TABLE cell;
IF EXISTS(SELECT TOP 1 * FROM sysObjects WHERE Id=OBJECT_ID(N'adjcell') and xtype='U')
	DROP TABLE adjcell;
IF EXISTS(SELECT TOP 1 * FROM sysObjects WHERE Id=OBJECT_ID(N'secadjcell') and xtype='U')
	DROP TABLE secadjcell;
IF EXISTS(SELECT TOP 1 * FROM sysObjects WHERE Id=OBJECT_ID(N'optcell') and xtype='U')
	DROP TABLE optcell;
IF EXISTS(SELECT TOP 1 * FROM sysObjects WHERE Id=OBJECT_ID(N'pciassignment') and xtype='U')
	DROP TABLE pciassignment;
IF EXISTS(SELECT TOP 1 * FROM sysObjects WHERE Id=OBJECT_ID(N'atudata') and xtype='U')
	DROP TABLE atudata;
IF EXISTS(SELECT TOP 1 * FROM sysObjects WHERE Id=OBJECT_ID(N'atuc2i') and xtype='U')
	DROP TABLE atuc2i;
IF EXISTS(SELECT TOP 1 * FROM sysObjects WHERE Id=OBJECT_ID(N'atuhandover') and xtype='U')
	DROP TABLE atuhandover;
IF EXISTS(SELECT TOP 1 * FROM sysObjects WHERE Id=OBJECT_ID(N'mrodata') and xtype='U')
	DROP TABLE mrodata;
IF EXISTS(SELECT TOP 1 * FROM sysObjects WHERE Id=OBJECT_ID(N'c2i') and xtype='U')
	DROP TABLE c2i;
IF EXISTS(SELECT TOP 1 * FROM sysObjects WHERE Id=OBJECT_ID(N'handover') and xtype='U')
	DROP TABLE handover;
IF EXISTS(SELECT TOP 1 * FROM sysObjects WHERE Id=OBJECT_ID(N'users') and xtype='U')
    DROP TABLE users;
IF EXISTS(SELECT TOP 1 * FROM sysObjects WHERE Id=OBJECT_ID(N'kpi') and xtype='U')
    DROP TABLE kpi;
IF EXISTS(SELECT TOP 1 * FROM sysObjects WHERE Id=OBJECT_ID(N'prb') and xtype='U')
    DROP TABLE prb;

CREATE TABLE enodeb
(
	city NVARCHAR(255) NULL,
	enodebid INT PRIMARY KEY,
	enodeb_name NVARCHAR(255) NOT NULL,
	vendor NVARCHAR(255),
	longitude FLOAT NOT NULL,
	latitude FLOAT NOT NULL,
	style NVARCHAR(255),
	CONSTRAINT chk_enodeb_vendor CHECK(vendor='华为' OR vendor='中兴' OR vendor='诺西' OR vendor='爱立信' OR vendor='贝尔' OR vendor='大唐'),
	CONSTRAINT chk_enodeb_style CHECK(style='宏站' OR style='室分' OR style='室外')
)
CREATE TABLE cell
(
	city NVARCHAR(255) NULL,
	sector_id NVARCHAR(255) PRIMARY KEY,
	sector_name NVARCHAR(255) NOT NULL,
	enodebid INT,
	enode_name NVARCHAR(255) NOT NULL,
	earfcn INT NOT NULL,
	pci INT NOT NULL,
	pss INT NULL,
	sss INT NULL,
	tac INT,
	azimuth FLOAT NOT NULL,
	height FLOAT,
	electtilt FLOAT,
	mechtilt FLOAT,
	totletilt FLOAT NOT NULL,
	CONSTRAINT fk_cell_enodeb_1 FOREIGN KEY (enodebid) REFERENCES enodeb(enodebid),
	CONSTRAINT chk_cell_pci CHECK(pci BETWEEN 0 AND 503),
	CONSTRAINT chk_cell_earfcn CHECK(earfcn=37900 OR earfcn=38098 OR earfcn=38400 OR earfcn=38544 OR earfcn=38496 OR earfcn=38950 OR earfcn=39148),
	CONSTRAINT chk_cell_pss CHECK(pss=0 OR pss=1 OR pss=2 OR pss=NULL),
	CONSTRAINT chk_cell_sss CHECK(sss=NULL OR sss BETWEEN 0 AND 167),
	CONSTRAINT chk_cell_totletilt CHECK(totletilt=electtilt+mechtilt),
)
CREATE TABLE adjcell
(
	s_sector_id VARCHAR(255),
	n_sector_id VARCHAR(255),
	s_earfcn INT,
	n_earfcn INT,
	PRIMARY KEY(s_sector_id, n_sector_id)
)
CREATE TABLE secadjcell
(
	s_sector_id VARCHAR(255),
	n_sector_id VARCHAR(255),
	PRIMARY KEY(s_sector_id, n_sector_id)
)
CREATE TABLE optcell
(
	sector_id NVARCHAR(50) PRIMARY KEY,
	earfcn INT,
	cell_type NVARCHAR(50),
	CONSTRAINT chk_optcell_earfcn CHECK(earfcn=37900 OR earfcn=38098 OR earfcn=38400 OR earfcn=38544 OR earfcn=38496 OR earfcn=38950 OR earfcn=39148),
	CONSTRAINT chk_optcell_celltype CHECK(cell_type='优化区' OR cell_type='保护带'),
)
CREATE TABLE pciassignment
(
	assign_id SMALLINT,
	earfcn INT,
	sector_id NVARCHAR(50),
	sector_name NVARCHAR(200),
	enodeb_id INT,
	pci INT,
	pss INT,
	sss INT,
	longitude FLOAT,
	latitude FLOAT,
	style VARCHAR(50),
	opt_datetime NVARCHAR(50),
	PRIMARY KEY(assign_id, sector_id),
	CONSTRAINT chk_pciassignment_earfcn CHECK(earfcn=37900 OR earfcn=38098 OR earfcn=38400 OR earfcn=38544 OR earfcn=38496 OR earfcn=38950 OR earfcn=39148),
	CONSTRAINT chk_pciassignment_style CHECK(style='宏站' OR style='室分' OR style='室外'),
)
CREATE TABLE atudata
(
	seq BIGINT,
	file_name NVARCHAR(255),
	time_stamp VARCHAR(100),
	longitude FLOAT,
	latitude FLOAT,
	cell_id NVARCHAR(50),
	tac INT,
	earfcn INT,
	pci SMALLINT,
	rsrp FLOAT,
	rs_sinr FLOAT,
	ncell_id_1 NVARCHAR(50),
	ncell_earfcn_1 INT,
	ncell_pci_1 SMALLINT,
	ncell_rsrp_1 FLOAT,
	ncell_id_2 NVARCHAR(50),
	ncell_earfcn_2 INT,
	ncell_pci_2 SMALLINT,
	ncell_rsrp_2 FLOAT,
	ncell_id_3 NVARCHAR(50),
	ncell_earfcn_3 INT,
	ncell_pci_3 SMALLINT,
	ncell_rsrp_3 FLOAT,
	ncell_id_4 NVARCHAR(50),
	ncell_earfcn_4 INT,
	ncell_pci_4 SMALLINT,
	ncell_rsrp_4 FLOAT,
	ncell_id_5 NVARCHAR(50),
	ncell_earfcn_5 INT,
	ncell_pci_5 SMALLINT,
	ncell_rsrp_5 FLOAT,
	ncell_id_6 NVARCHAR(50),
	ncell_earfcn_6 INT,
	ncell_pci_6 SMALLINT,
	ncell_rsrp_6 FLOAT,
	PRIMARY KEY(seq, file_name)
)
CREATE TABLE atuc2i
(
	sector_id NVARCHAR(50),
	ncell_id NVARCHAR(50),
	ratio_all FLOAT,
	rank INT,
	cosite TINYINT,
	PRIMARY KEY(ncell_id, sector_id)
)
CREATE TABLE atuhandover
(
	s_sector_id NVARCHAR(50),
	n_sector_id NVARCHAR(50),
	hoatt INT,
	PRIMARY KEY(s_sector_id, n_sector_id)
)
CREATE TABLE mrodata
(
	time_stamp NVARCHAR(30),
	serving_sector NVARCHAR(50),
	interfering_sector NVARCHAR(50),
	lte_sc_rsrp FLOAT,
	lte_nc_rsrp FLOAT,
	lte_nc_earfcn INT,
	lte_nc_pci SMALLINT,
	PRIMARY KEY(time_stamp, serving_sector, interfering_sector)
)
CREATE TABLE c2i
(
	city NVARCHAR(255),
	scell_id NVARCHAR(255),
	ncell_id NVARCHAR(255),
	prc2i9 FLOAT,
	c2i_mean FLOAT,
	std FLOAT,
	samplecount FLOAT,
	weightedc2i FLOAT,
	PRIMARY KEY(scell_id, ncell_id)
)
CREATE TABLE handover
(
	city NVARCHAR(255),
	scell_id VARCHAR(50),
	ncell_id VARCHAR(50),
	hoatt INT,
	hosucc INT,
	hosuccrate FLOAT,
	PRIMARY KEY(scell_id, ncell_id)
)
CREATE TABLE users
(
    account VARCHAR(50),
    authentication CHAR(32),
    PRIMARY KEY(account)
)
CREATE TABLE kpi
(
    timestamp VARCHAR(10),
    enb_name NVARCHAR(50),
    sector_name NVARCHAR(50),
    rrc_conn_succ_rate FLOAT,
    erab_succ_rate FLOAT,
    erab_drop_rate FLOAT,
    wireless_conn FLOAT,
    wireless_drop FLOAT,
    enb_inter FLOAT,
    enb_outer FLOAT,
    same_freq_handover FLOAT,
    diff_freq_handover FLOAT,
    handover_rate FLOAT,
    pdcp_upper BIGINT,
    pdcp_down BIGINT,
    rrc_rebuild FLOAT,
    enb_handout_succ INT,
    enb_handout_req INT,
    PRIMARY KEY(enb_name, timestamp, sector_name)
)
CREATE TABLE prb
(
    timestamp VARCHAR(20),
    enb_name NVARCHAR(50),
    sector_name NVARCHAR(50),
    prb0 INT,
    prb1 INT,
    prb2 INT,
    prb3 INT,
    prb4 INT,
    prb5 INT,
    prb6 INT,
    prb7 INT,
    prb8 INT,
    prb9 INT,
    prb10 INT,
    prb11 INT,
    prb12 INT,
    prb13 INT,
    prb14 INT,
    prb15 INT,
    prb16 INT,
    prb17 INT,
    prb18 INT,
    prb19 INT,
    prb20 INT,
    prb21 INT,
    prb22 INT,
    prb23 INT,
    prb24 INT,
    prb25 INT,
    prb26 INT,
    prb27 INT,
    prb28 INT,
    prb29 INT,
    prb30 INT,
    prb31 INT,
    prb32 INT,
    prb33 INT,
    prb34 INT,
    prb35 INT,
    prb36 INT,
    prb37 INT,
    prb38 INT,
    prb39 INT,
    prb40 INT,
    prb41 INT,
    prb42 INT,
    prb43 INT,
    prb44 INT,
    prb45 INT,
    prb46 INT,
    prb47 INT,
    prb48 INT,
    prb49 INT,
    prb50 INT,
    prb51 INT,
    prb52 INT,
    prb53 INT,
    prb54 INT,
    prb55 INT,
    prb56 INT,
    prb57 INT,
    prb58 INT,
    prb59 INT,
    prb60 INT,
    prb61 INT,
    prb62 INT,
    prb63 INT,
    prb64 INT,
    prb65 INT,
    prb66 INT,
    prb67 INT,
    prb68 INT,
    prb69 INT,
    prb70 INT,
    prb71 INT,
    prb72 INT,
    prb73 INT,
    prb74 INT,
    prb75 INT,
    prb76 INT,
    prb77 INT,
    prb78 INT,
    prb79 INT,
    prb80 INT,
    prb81 INT,
    prb82 INT,
    prb83 INT,
    prb84 INT,
    prb85 INT,
    prb86 INT,
    prb87 INT,
    prb88 INT,
    prb89 INT,
    prb90 INT,
    prb91 INT,
    prb92 INT,
    prb93 INT,
    prb94 INT,
    prb95 INT,
    prb96 INT,
    prb97 INT,
    prb98 INT,
    prb99 INT,
    PRIMARY KEY(timestamp, enb_name, sector_name)
)

IF EXISTS (select * from sys.triggers where name='trig_enodeb')
BEGIN
    DROP TRIGGER trig_enodeb
END

IF EXISTS (select * from sys.triggers where name='trig_adjcell')
BEGIN
    DROP TRIGGER trig_adjcell
END

IF EXISTS (select * from sys.triggers where name='trig_atuc2i')
BEGIN
    DROP TRIGGER trig_atuc2i
END

IF EXISTS (select * from sys.triggers where name='trig_atudata')
BEGIN
    DROP TRIGGER trig_atudata
END

IF EXISTS (select * from sys.triggers where name='trig_atuhandover')
BEGIN
    DROP TRIGGER trig_atuhandover
END

IF EXISTS (select * from sys.triggers where name='trig_c2i')
BEGIN
    DROP TRIGGER trig_c2i
END

IF EXISTS (select * from sys.triggers where name='trig_cell')
BEGIN
    DROP TRIGGER trig_cell
END

IF EXISTS (select * from sys.triggers where name='trig_handover')
BEGIN
    DROP TRIGGER trig_handover
END

IF EXISTS (select * from sys.triggers where name='trig_kpi')
BEGIN
    DROP TRIGGER trig_kpi
END

IF EXISTS (select * from sys.triggers where name='trig_mrodata')
BEGIN
    DROP TRIGGER trig_mrodata
END

IF EXISTS (select * from sys.triggers where name='trig_optcell')
BEGIN
    DROP TRIGGER trig_optcell
END

IF EXISTS (select * from sys.triggers where name='trig_pciassignment')
BEGIN
    DROP TRIGGER trig_pciassignment
END

IF EXISTS (select * from sys.triggers where name='trig_prb')
BEGIN
    DROP TRIGGER trig_prb
END

IF EXISTS (select * from sys.triggers where name='trig_secadjcell')
BEGIN
    DROP TRIGGER trig_secadjcell
END