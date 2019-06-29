-- Initialize the database.
-- Drop any existing data and create empty tables.

/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2019/6/16 23:09:25                           */
/*==============================================================*/


drop table if exists Account;

drop table if exists Bank;

drop table if exists CheckAccount;

drop table if exists Client;

drop table if exists Owning;

drop table if exists LinkMan;

drop table if exists Loan;

drop table if exists OpenAccount;

drop table if exists PayLoan;

drop table if exists PersonInCharge;

drop table if exists SaveAccount;

drop table if exists Staff;

/*==============================================================*/
/* Table: Account                                               */
/*==============================================================*/
create table Account
(
   AccountID            char(11) not null,
   Balance              float not null,
   DateOpening          date not null,
   primary key (AccountID)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

/*==============================================================*/
/* Table: Bank                                                  */
/*==============================================================*/
create table Bank
(
   BankName             char(255) not null,
   City                 char(255) not null,
   Property             int not null,
   primary key (BankName)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

/*==============================================================*/
/* Table: CheckAccount                                          */
/*==============================================================*/
create table CheckAccount
(
   AccountID            char(11) not null,
   BankName             char(255) not null,
   ClientID             char(18) not null,
   Balance              float not null,
   DateOpening          date not null,
   Overdraft            float not null,
   primary key (AccountID)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

/*==============================================================*/
/* Table: Client                                                */
/*==============================================================*/
create table Client
(
   ClientID             char(18) not null,
   LinkID               char(18),
   LinkName             char(16),
   ClientName           char(18) not null,
   Phone                char(14) not null,
   Address              char(255) not null,
   primary key (ClientID)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

/*==============================================================*/
/* Table: Owning                                              */
/*==============================================================*/
create table Owning
(
   ClientID             char(18) not null,
   LoanID               char(18) not null,
   primary key (ClientID, LoanID)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

/*==============================================================*/
/* Table: LinkMan                                               */
/*==============================================================*/
create table LinkMan
(
   ClientID             char(18) not null,
   LinkName             char(16) not null,
   Phone                char(14) not null,
   Email                char(18) not null,
   Association          char(128) not null,
   primary key (ClientID, LinkName)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

/*==============================================================*/
/* Table: Loan                                                  */
/*==============================================================*/
create table Loan
(
   LoanID               char(18) not null,
   BankName             char(255),
   Amount               float not null,
   primary key (LoanID)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

/*==============================================================*/
/* Table: OpenAccount                                           */
/*==============================================================*/
create table OpenAccount
(
   BankName             char(255) not null,
   ClientID             char(18) not null,
   CheckAccountID       char(11),
   SaveAccountID        char(11),
   primary key (BankName, ClientID)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

/*==============================================================*/
/* Table: PayLoan                                               */
/*==============================================================*/
create table PayLoan
(
   LoanID               char(18) not null,
   Date                 date not null,
   Amount               float not null,
   primary key (LoanID)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

/*==============================================================*/
/* Table: PersonInCharge                                        */
/*==============================================================*/
create table PersonInCharge
(
   ClientID             char(18) not null,
   StaffID              char(18) not null,
   ChargeType           bool not null,
   primary key (ClientID, StaffID)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

/*==============================================================*/
/* Table: SaveAccount                                           */
/*==============================================================*/
create table SaveAccount
(
   AccountID            char(11) not null,
   BankName             char(255) not null,
   ClientID             char(18) not null,
   Balance              float not null,
   DateOpening          date not null,
   Rate                 float not null,
   MoneyType            char(10) not null,
   primary key (AccountID)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

/*==============================================================*/
/* Table: Staff                                                 */
/*==============================================================*/
create table Staff
(
   StaffID              char(18) not null,
   BankName             char(255),
   StaffName            char(18) not null,
   Phone                char(14) not null,
   Address              char(255) not null,
   DateStartWorking     date not null,
   primary key (StaffID)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

alter table CheckAccount add constraint FK_Relationship_15 foreign key (BankName, ClientID)
      references OpenAccount (BankName, ClientID) on delete restrict on update restrict;

alter table CheckAccount add constraint FK_AccountType foreign key (AccountID)
      references Account (AccountID) on delete restrict on update restrict;

alter table Client add constraint FK_Link foreign key (LinkID, LinkName)
      references LinkMan (ClientID, LinkName) on delete restrict on update restrict;

alter table Owning add constraint FK_Owning foreign key (ClientID)
      references Client (ClientID) on delete restrict on update restrict;

alter table Owning add constraint FK_Owning2 foreign key (LoanID)
      references Loan (LoanID) on delete restrict on update restrict;

alter table LinkMan add constraint FK_Link2 foreign key (ClientID)
      references Client (ClientID) on delete restrict on update restrict;

alter table Loan add constraint FK_Send foreign key (BankName)
      references Bank (BankName) on delete restrict on update restrict;

alter table OpenAccount add constraint FK_Relationship_13 foreign key (BankName)
      references Bank (BankName) on delete restrict on update restrict;

alter table OpenAccount add constraint FK_Relationship_14 foreign key (ClientID)
      references Client (ClientID) on delete restrict on update restrict;

alter table OpenAccount add constraint FK_Relationship_16 foreign key (SaveAccountID)
      references CheckAccount (AccountID) on delete restrict on update restrict;

alter table OpenAccount add constraint FK_Relationship_18 foreign key (CheckAccountID)
      references SaveAccount (AccountID) on delete restrict on update restrict;

alter table PayLoan add constraint FK_PayInstalments foreign key (LoanID)
      references Loan (LoanID) on delete restrict on update restrict;

alter table PersonInCharge add constraint FK_Charge foreign key (ClientID)
      references Client (ClientID) on delete restrict on update restrict;

alter table PersonInCharge add constraint FK_Charge2 foreign key (StaffID)
      references Staff (StaffID) on delete restrict on update restrict;

alter table SaveAccount add constraint FK_Relationship_17 foreign key (BankName, ClientID)
      references OpenAccount (BankName, ClientID) on delete restrict on update restrict;

alter table SaveAccount add constraint FK_AccountType2 foreign key (AccountID)
      references Account (AccountID) on delete restrict on update restrict;

alter table Staff add constraint FK_WorkOn foreign key (BankName)
      references Bank (BankName) on delete restrict on update restrict;
