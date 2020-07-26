CREATE trigger trig_atudata
ON atudata
INSTEAD OF INSERT
AS
BEGIN
IF EXISTS(SELECT seq FROM inserted)  --插入和更新
    DECLARE cur CURSOR forward_only
    FOR SELECT seq, file_name, time_stamp, longitude, latitude,
    cell_id, tac, earfcn, pci, rsrp, rs_sinr,
    ncell_id_1, ncell_earfcn_1, ncell_pci_1, ncell_rsrp_1,
    ncell_id_2, ncell_earfcn_2, ncell_pci_2, ncell_rsrp_2,
    ncell_id_3, ncell_earfcn_3, ncell_pci_3, ncell_rsrp_3,
    ncell_id_4, ncell_earfcn_4, ncell_pci_4, ncell_rsrp_4,
    ncell_id_5, ncell_earfcn_5, ncell_pci_5, ncell_rsrp_5,
    ncell_id_6, ncell_earfcn_6, ncell_pci_6, ncell_rsrp_6 FROM inserted
    OPEN cur  --打开游标
    DECLARE @seq BIGINT
    DECLARE @file_name NVARCHAR(255)
    DECLARE @time_stamp VARCHAR(100)
    DECLARE @longitude FLOAT
    DECLARE @latitude FLOAT
    DECLARE @cell_id NVARCHAR(50)
    DECLARE @tac INT
    DECLARE @earfcn INT
    DECLARE @pci SMALLINT
    DECLARE @rsrp FLOAT
    DECLARE @rs_sinr FLOAT
    DECLARE @ncell_id_1 NVARCHAR(50)
    DECLARE @ncell_earfcn_1 INT
    DECLARE @ncell_pci_1 SMALLINT
    DECLARE @ncell_rsrp_1 FLOAT
    DECLARE @ncell_id_2 NVARCHAR(50)
    DECLARE @ncell_earfcn_2 INT
    DECLARE @ncell_pci_2 SMALLINT
    DECLARE @ncell_rsrp_2 FLOAT
    DECLARE @ncell_id_3 NVARCHAR(50)
    DECLARE @ncell_earfcn_3 INT
    DECLARE @ncell_pci_3 SMALLINT
    DECLARE @ncell_rsrp_3 FLOAT
    DECLARE @ncell_id_4 NVARCHAR(50)
    DECLARE @ncell_earfcn_4 INT
    DECLARE @ncell_pci_4 SMALLINT
    DECLARE @ncell_rsrp_4 FLOAT
    DECLARE @ncell_id_5 NVARCHAR(50)
    DECLARE @ncell_earfcn_5 INT
    DECLARE @ncell_pci_5 SMALLINT
    DECLARE @ncell_rsrp_5 FLOAT
    DECLARE @ncell_id_6 NVARCHAR(50)
    DECLARE @ncell_earfcn_6 INT
    DECLARE @ncell_pci_6 SMALLINT
    DECLARE @ncell_rsrp_6 FLOAT
    FETCH NEXT FROM cur INTO @seq, @file_name, @time_stamp, @longitude,
    @latitude, @cell_id, @tac, @earfcn, @pci, @rsrp, @rs_sinr,
    @ncell_id_1, @ncell_earfcn_1, @ncell_pci_1, @ncell_rsrp_1,
    @ncell_id_2, @ncell_earfcn_2, @ncell_pci_2, @ncell_rsrp_2,
    @ncell_id_3, @ncell_earfcn_3, @ncell_pci_3, @ncell_rsrp_3,
    @ncell_id_4, @ncell_earfcn_4, @ncell_pci_4, @ncell_rsrp_4,
    @ncell_id_5, @ncell_earfcn_5, @ncell_pci_5, @ncell_rsrp_5,
    @ncell_id_6, @ncell_earfcn_6, @ncell_pci_6, @ncell_rsrp_6
    WHILE(@@FETCH_STATUS=0)
    BEGIN
        --增加操作
        IF (@ncell_id_1='null') BEGIN SET @ncell_id_1=null END
        IF (@ncell_id_2='null') BEGIN SET @ncell_id_2=null END
        IF (@ncell_id_3='null') BEGIN SET @ncell_id_3=null END
        IF (@ncell_id_4='null') BEGIN SET @ncell_id_4=null END
        IF (@ncell_id_5='null') BEGIN SET @ncell_id_5=null END
        IF (@ncell_id_6='null') BEGIN SET @ncell_id_6=null END
        IF (@ncell_earfcn_1=-1) BEGIN SET @ncell_earfcn_1=null END
        IF (@ncell_earfcn_2=-1) BEGIN SET @ncell_earfcn_2=null END
        IF (@ncell_earfcn_3=-1) BEGIN SET @ncell_earfcn_3=null END
        IF (@ncell_earfcn_4=-1) BEGIN SET @ncell_earfcn_4=null END
        IF (@ncell_earfcn_5=-1) BEGIN SET @ncell_earfcn_5=null END
        IF (@ncell_earfcn_6=-1) BEGIN SET @ncell_earfcn_6=null END
        IF (@ncell_pci_1=-1) BEGIN SET @ncell_pci_1=null END
        IF (@ncell_pci_2=-1) BEGIN SET @ncell_pci_2=null END
        IF (@ncell_pci_3=-1) BEGIN SET @ncell_pci_3=null END
        IF (@ncell_pci_4=-1) BEGIN SET @ncell_pci_4=null END
        IF (@ncell_pci_5=-1) BEGIN SET @ncell_pci_5=null END
        IF (@ncell_pci_6=-1) BEGIN SET @ncell_pci_6=null END
        IF (@ncell_rsrp_1=-1) BEGIN SET @ncell_rsrp_1=null END
        IF (@ncell_rsrp_2=-1) BEGIN SET @ncell_rsrp_2=null END
        IF (@ncell_rsrp_3=-1) BEGIN SET @ncell_rsrp_3=null END
        IF (@ncell_rsrp_4=-1) BEGIN SET @ncell_rsrp_4=null END
        IF (@ncell_rsrp_5=-1) BEGIN SET @ncell_rsrp_5=null END
        IF (@ncell_rsrp_6=-1) BEGIN SET @ncell_rsrp_6=null END
        IF ((SELECT COUNT (*) FROM atudata WHERE seq=@seq AND file_name=@file_name)<1)
        BEGIN
            INSERT INTO atudata VALUES (@seq, @file_name, @time_stamp, @longitude,
            @latitude, @cell_id, @tac, @earfcn, @pci, @rsrp, @rs_sinr,
            @ncell_id_1, @ncell_earfcn_1, @ncell_pci_1, @ncell_rsrp_1,
            @ncell_id_2, @ncell_earfcn_2, @ncell_pci_2, @ncell_rsrp_2,
            @ncell_id_3, @ncell_earfcn_3, @ncell_pci_3, @ncell_rsrp_3,
            @ncell_id_4, @ncell_earfcn_4, @ncell_pci_4, @ncell_rsrp_4,
            @ncell_id_5, @ncell_earfcn_5, @ncell_pci_5, @ncell_rsrp_5,
            @ncell_id_6, @ncell_earfcn_6, @ncell_pci_6, @ncell_rsrp_6)
        END
        ELSE
        BEGIN
            UPDATE atudata SET
            time_stamp=@time_stamp,
            longitude=@longitude,
            latitude=@latitude,
            cell_id=@cell_id,
            tac=@tac,
            earfcn=@earfcn,
            pci=@pci,
            rsrp=@rsrp,
            rs_sinr=@rs_sinr,
            ncell_id_1=@ncell_id_1,
            ncell_earfcn_1=@ncell_earfcn_1,
            ncell_pci_1=@ncell_pci_1,
            ncell_rsrp_1=@ncell_rsrp_1,
            ncell_id_2=@ncell_id_2,
            ncell_earfcn_2=@ncell_earfcn_2,
            ncell_pci_2=@ncell_pci_2,
            ncell_rsrp_2=@ncell_rsrp_2,
            ncell_id_3=@ncell_id_3,
            ncell_earfcn_3=@ncell_earfcn_3,
            ncell_pci_3=@ncell_pci_3,
            ncell_rsrp_3=@ncell_rsrp_3,
            ncell_id_4=@ncell_id_4,
            ncell_earfcn_4=@ncell_earfcn_4,
            ncell_pci_4=@ncell_pci_4,
            ncell_rsrp_4=@ncell_rsrp_4,
            ncell_id_5=@ncell_id_5,
            ncell_earfcn_5=@ncell_earfcn_5,
            ncell_pci_5=@ncell_pci_5,
            ncell_rsrp_5=@ncell_rsrp_5,
            ncell_id_6=@ncell_id_6,
            ncell_earfcn_6=@ncell_earfcn_6,
            ncell_pci_6=@ncell_pci_6,
            ncell_rsrp_6=@ncell_rsrp_6
            WHERE seq=@seq AND file_name=@file_name
        END
        FETCH NEXT FROM cur INTO @seq, @file_name, @time_stamp, @longitude,
        @latitude, @cell_id, @tac, @earfcn, @pci, @rsrp, @rs_sinr,
        @ncell_id_1, @ncell_earfcn_1, @ncell_pci_1, @ncell_rsrp_1,
        @ncell_id_2, @ncell_earfcn_2, @ncell_pci_2, @ncell_rsrp_2,
        @ncell_id_3, @ncell_earfcn_3, @ncell_pci_3, @ncell_rsrp_3,
        @ncell_id_4, @ncell_earfcn_4, @ncell_pci_4, @ncell_rsrp_4,
        @ncell_id_5, @ncell_earfcn_5, @ncell_pci_5, @ncell_rsrp_5,
        @ncell_id_6, @ncell_earfcn_6, @ncell_pci_6, @ncell_rsrp_6   --指向下一条
    END
    CLOSE cur  --关闭游标
    DEALLOCATE cur  --销毁游标资源
END