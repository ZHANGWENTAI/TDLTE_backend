CREATE trigger trig_prb ON prb
INSTEAD OF INSERT
AS
BEGIN
IF EXISTS(SELECT enb_name FROM inserted)  --插入和更新
    DECLARE cur CURSOR forward_only FOR SELECT * FROM inserted
    OPEN cur
    DECLARE @time_stamp VARCHAR(50)
    DECLARE @enb_name NVARCHAR(50)
    DECLARE @sector_name NVARCHAR(50)
    DECLARE @prb0 INT
    DECLARE @prb1 INT
    DECLARE @prb2 INT
    DECLARE @prb3 INT
    DECLARE @prb4 INT
    DECLARE @prb5 INT
    DECLARE @prb6 INT
    DECLARE @prb7 INT
    DECLARE @prb8 INT
    DECLARE @prb9 INT
    DECLARE @prb10 INT
    DECLARE @prb11 INT
    DECLARE @prb12 INT
    DECLARE @prb13 INT
    DECLARE @prb14 INT
    DECLARE @prb15 INT
    DECLARE @prb16 INT
    DECLARE @prb17 INT
    DECLARE @prb18 INT
    DECLARE @prb19 INT
    DECLARE @prb20 INT
    DECLARE @prb21 INT
    DECLARE @prb22 INT
    DECLARE @prb23 INT
    DECLARE @prb24 INT
    DECLARE @prb25 INT
    DECLARE @prb26 INT
    DECLARE @prb27 INT
    DECLARE @prb28 INT
    DECLARE @prb29 INT
    DECLARE @prb30 INT
    DECLARE @prb31 INT
    DECLARE @prb32 INT
    DECLARE @prb33 INT
    DECLARE @prb34 INT
    DECLARE @prb35 INT
    DECLARE @prb36 INT
    DECLARE @prb37 INT
    DECLARE @prb38 INT
    DECLARE @prb39 INT
    DECLARE @prb40 INT
    DECLARE @prb41 INT
    DECLARE @prb42 INT
    DECLARE @prb43 INT
    DECLARE @prb44 INT
    DECLARE @prb45 INT
    DECLARE @prb46 INT
    DECLARE @prb47 INT
    DECLARE @prb48 INT
    DECLARE @prb49 INT
    DECLARE @prb50 INT
    DECLARE @prb51 INT
    DECLARE @prb52 INT
    DECLARE @prb53 INT
    DECLARE @prb54 INT
    DECLARE @prb55 INT
    DECLARE @prb56 INT
    DECLARE @prb57 INT
    DECLARE @prb58 INT
    DECLARE @prb59 INT
    DECLARE @prb60 INT
    DECLARE @prb61 INT
    DECLARE @prb62 INT
    DECLARE @prb63 INT
    DECLARE @prb64 INT
    DECLARE @prb65 INT
    DECLARE @prb66 INT
    DECLARE @prb67 INT
    DECLARE @prb68 INT
    DECLARE @prb69 INT
    DECLARE @prb70 INT
    DECLARE @prb71 INT
    DECLARE @prb72 INT
    DECLARE @prb73 INT
    DECLARE @prb74 INT
    DECLARE @prb75 INT
    DECLARE @prb76 INT
    DECLARE @prb77 INT
    DECLARE @prb78 INT
    DECLARE @prb79 INT
    DECLARE @prb80 INT
    DECLARE @prb81 INT
    DECLARE @prb82 INT
    DECLARE @prb83 INT
    DECLARE @prb84 INT
    DECLARE @prb85 INT
    DECLARE @prb86 INT
    DECLARE @prb87 INT
    DECLARE @prb88 INT
    DECLARE @prb89 INT
    DECLARE @prb90 INT
    DECLARE @prb91 INT
    DECLARE @prb92 INT
    DECLARE @prb93 INT
    DECLARE @prb94 INT
    DECLARE @prb95 INT
    DECLARE @prb96 INT
    DECLARE @prb97 INT
    DECLARE @prb98 INT
    DECLARE @prb99 INT
    FETCH NEXT FROM cur INTO
    @time_stamp,
    @enb_name,
    @sector_name,
    @prb0,
    @prb1,
    @prb2,
    @prb3,
    @prb4,
    @prb5,
    @prb6,
    @prb7,
    @prb8,
    @prb9,
    @prb10,
    @prb11,
    @prb12,
    @prb13,
    @prb14,
    @prb15,
    @prb16,
    @prb17,
    @prb18,
    @prb19,
    @prb20,
    @prb21,
    @prb22,
    @prb23,
    @prb24,
    @prb25,
    @prb26,
    @prb27,
    @prb28,
    @prb29,
    @prb30,
    @prb31,
    @prb32,
    @prb33,
    @prb34,
    @prb35,
    @prb36,
    @prb37,
    @prb38,
    @prb39,
    @prb40,
    @prb41,
    @prb42,
    @prb43,
    @prb44,
    @prb45,
    @prb46,
    @prb47,
    @prb48,
    @prb49,
    @prb50,
    @prb51,
    @prb52,
    @prb53,
    @prb54,
    @prb55,
    @prb56,
    @prb57,
    @prb58,
    @prb59,
    @prb60,
    @prb61,
    @prb62,
    @prb63,
    @prb64,
    @prb65,
    @prb66,
    @prb67,
    @prb68,
    @prb69,
    @prb70,
    @prb71,
    @prb72,
    @prb73,
    @prb74,
    @prb75,
    @prb76,
    @prb77,
    @prb78,
    @prb79,
    @prb80,
    @prb81,
    @prb82,
    @prb83,
    @prb84,
    @prb85,
    @prb86,
    @prb87,
    @prb88,
    @prb89,
    @prb90,
    @prb91,
    @prb92,
    @prb93,
    @prb94,
    @prb95,
    @prb96,
    @prb97,
    @prb98,
    @prb99
    BEGIN
        --增加操作
    IF ((SELECT COUNT (*) FROM prb WHERE enb_name=@enb_name AND time_stamp=@time_stamp AND sector_name=@sector_name)<1)
    BEGIN
        INSERT INTO prb VALUES (@time_stamp, @enb_name, @sector_name,
        @prb0,
        @prb1,
        @prb2,
        @prb3,
        @prb4,
        @prb5,
        @prb6,
        @prb7,
        @prb8,
        @prb9,
        @prb10,
        @prb11,
        @prb12,
        @prb13,
        @prb14,
        @prb15,
        @prb16,
        @prb17,
        @prb18,
        @prb19,
        @prb20,
        @prb21,
        @prb22,
        @prb23,
        @prb24,
        @prb25,
        @prb26,
        @prb27,
        @prb28,
        @prb29,
        @prb30,
        @prb31,
        @prb32,
        @prb33,
        @prb34,
        @prb35,
        @prb36,
        @prb37,
        @prb38,
        @prb39,
        @prb40,
        @prb41,
        @prb42,
        @prb43,
        @prb44,
        @prb45,
        @prb46,
        @prb47,
        @prb48,
        @prb49,
        @prb50,
        @prb51,
        @prb52,
        @prb53,
        @prb54,
        @prb55,
        @prb56,
        @prb57,
        @prb58,
        @prb59,
        @prb60,
        @prb61,
        @prb62,
        @prb63,
        @prb64,
        @prb65,
        @prb66,
        @prb67,
        @prb68,
        @prb69,
        @prb70,
        @prb71,
        @prb72,
        @prb73,
        @prb74,
        @prb75,
        @prb76,
        @prb77,
        @prb78,
        @prb79,
        @prb80,
        @prb81,
        @prb82,
        @prb83,
        @prb84,
        @prb85,
        @prb86,
        @prb87,
        @prb88,
        @prb89,
        @prb90,
        @prb91,
        @prb92,
        @prb93,
        @prb94,
        @prb95,
        @prb96,
        @prb97,
        @prb98,
        @prb99)
    END
    ELSE
    BEGIN
        UPDATE prb SET
        prb0=@prb0,
        prb1=@prb1,
        prb2=@prb2,
        prb3=@prb3,
        prb4=@prb4,
        prb5=@prb5,
        prb6=@prb6,
        prb7=@prb7,
        prb8=@prb8,
        prb9=@prb9,
        prb10=@prb10,
        prb11=@prb11,
        prb12=@prb12,
        prb13=@prb13,
        prb14=@prb14,
        prb15=@prb15,
        prb16=@prb16,
        prb17=@prb17,
        prb18=@prb18,
        prb19=@prb19,
        prb20=@prb20,
        prb21=@prb21,
        prb22=@prb22,
        prb23=@prb23,
        prb24=@prb24,
        prb25=@prb25,
        prb26=@prb26,
        prb27=@prb27,
        prb28=@prb28,
        prb29=@prb29,
        prb30=@prb30,
        prb31=@prb31,
        prb32=@prb32,
        prb33=@prb33,
        prb34=@prb34,
        prb35=@prb35,
        prb36=@prb36,
        prb37=@prb37,
        prb38=@prb38,
        prb39=@prb39,
        prb40=@prb40,
        prb41=@prb41,
        prb42=@prb42,
        prb43=@prb43,
        prb44=@prb44,
        prb45=@prb45,
        prb46=@prb46,
        prb47=@prb47,
        prb48=@prb48,
        prb49=@prb49,
        prb50=@prb50,
        prb51=@prb51,
        prb52=@prb52,
        prb53=@prb53,
        prb54=@prb54,
        prb55=@prb55,
        prb56=@prb56,
        prb57=@prb57,
        prb58=@prb58,
        prb59=@prb59,
        prb60=@prb60,
        prb61=@prb61,
        prb62=@prb62,
        prb63=@prb63,
        prb64=@prb64,
        prb65=@prb65,
        prb66=@prb66,
        prb67=@prb67,
        prb68=@prb68,
        prb69=@prb69,
        prb70=@prb70,
        prb71=@prb71,
        prb72=@prb72,
        prb73=@prb73,
        prb74=@prb74,
        prb75=@prb75,
        prb76=@prb76,
        prb77=@prb77,
        prb78=@prb78,
        prb79=@prb79,
        prb80=@prb80,
        prb81=@prb81,
        prb82=@prb82,
        prb83=@prb83,
        prb84=@prb84,
        prb85=@prb85,
        prb86=@prb86,
        prb87=@prb87,
        prb88=@prb88,
        prb89=@prb89,
        prb90=@prb90,
        prb91=@prb91,
        prb92=@prb92,
        prb93=@prb93,
        prb94=@prb94,
        prb95=@prb95,
        prb96=@prb96,
        prb97=@prb97,
        prb98=@prb98,
        prb99=@prb99
        WHERE enb_name=@enb_name AND time_stamp=@time_stamp AND sector_name=@sector_name
    END
    FETCH NEXT FROM cur INTO  @enb_name, @time_stamp, @sector_name,
        @prb0,
        @prb1,
        @prb2,
        @prb3,
        @prb4,
        @prb5,
        @prb6,
        @prb7,
        @prb8,
        @prb9,
        @prb10,
        @prb11,
        @prb12,
        @prb13,
        @prb14,
        @prb15,
        @prb16,
        @prb17,
        @prb18,
        @prb19,
        @prb20,
        @prb21,
        @prb22,
        @prb23,
        @prb24,
        @prb25,
        @prb26,
        @prb27,
        @prb28,
        @prb29,
        @prb30,
        @prb31,
        @prb32,
        @prb33,
        @prb34,
        @prb35,
        @prb36,
        @prb37,
        @prb38,
        @prb39,
        @prb40,
        @prb41,
        @prb42,
        @prb43,
        @prb44,
        @prb45,
        @prb46,
        @prb47,
        @prb48,
        @prb49,
        @prb50,
        @prb51,
        @prb52,
        @prb53,
        @prb54,
        @prb55,
        @prb56,
        @prb57,
        @prb58,
        @prb59,
        @prb60,
        @prb61,
        @prb62,
        @prb63,
        @prb64,
        @prb65,
        @prb66,
        @prb67,
        @prb68,
        @prb69,
        @prb70,
        @prb71,
        @prb72,
        @prb73,
        @prb74,
        @prb75,
        @prb76,
        @prb77,
        @prb78,
        @prb79,
        @prb80,
        @prb81,
        @prb82,
        @prb83,
        @prb84,
        @prb85,
        @prb86,
        @prb87,
        @prb88,
        @prb89,
        @prb90,
        @prb91,
        @prb92,
        @prb93,
        @prb94,
        @prb95,
        @prb96,
        @prb97,
        @prb98,
        @prb99  --指向下一条
    END
    CLOSE cur  --关闭游标
    DEALLOCATE cur  --销毁游标资源
END