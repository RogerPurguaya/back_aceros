# -*- encoding: utf-8 -*-
{
	'name': 'Account Purchase Register IT',
	'category': 'account',
	'author': 'ITGRUPO-COMPATIBLE-BO',
	'depends': ['import_base_it','account_registro_compra_it'],
	'version': '1.0',
	'description':"""
A) PARA CREAR EL REGISTRO DE COMPRAS  ES NECESARIO  AGREGAR  LA OPCION ISC Y  OTROS AL COMBOBOX TIPO DE COMPRA  QUE ESTA EN LOS CÓDIGOS DE IMPUESTOS 												
B) CADA VEZ QUE SE REGISTRA UN ASIENTO CONTABLE EN LA COLUMNA CUENTA IMPUESTOS SE GRABA EL ID DEL IMPUESTO QUE SE ELIGIO  Y EN LA COLUMNA 												
IMPORTE IMPUESTO BASE  SE GRABAN LOS MONTOS QUE LE CORRESPONDE A LA BASE Y AL IMPUESTO.   AHORA TANTO LA BASE COMO EL IMPUESTO ESTAN RELACIONADOS 												
A UN CODIGO DE IMPUESTO  QUE A SU VEZ TIENE UN TIPO DE COMPRA  QUE ES LA QUE NOS VA A SERVIR PARA  SABER A QUE COLUMNA VA ESE IMPORTE;  SI TOMAMOS COMO 												
EJEMPLO LA IMAGEN1  ADJUNTA  TENDRIAMOS LO SIGUIENTE : 												
												
EMPRESA	COMPROBANTE	CUENTA IMPUESTO	"IMPORTE 
IMPUESTO 
BASE"	"TIPO 
DOCUMENTO"	"TIPO DE CAMBIO
SUNAT"	TIPO COMPRA						
PROVESUR SRL	0001-7765	"IMPUESTO PAGADO 
IGV"	2070	01	0	DESTINADO A OPERACIONES GRAVADAS Y/O DE EXPORTACION				1		
PROVESUR SRL	0001-7765	"COMPRAS GRAVADAS
CON IGV"	3000	01	0	DESTINADO A OPERACIONES GRAVADAS Y/O DE EXPORTACION				1		
PROVESUR SRL	0001-7765	"COMPRAS GRAVADAS
CON IGV"	4500	01	0	DESTINADO A OPERACIONES GRAVADAS Y/O DE EXPORTACION				1		
PROVESUR SRL	0001-7765	"COMPRAS GRAVADAS
CON IGV"	4000	01	0	DESTINADO A OPERACIONES GRAVADAS Y/O DE EXPORTACION				1		
												
												
RESUMIENDO ESTO TENDRÍAMOS  NUESTRO REGISTRO DE COMPRAS DE ESTA FORMA :  												
											1	2
Periodo	Vou	Fecha E.	Fecha V.	TD	Serie	Año	Numero	TDP	RUC/DNI	Razon Social	BIOGE	BIOGENG
01/01	COM-4	05/01/2015	05/01/2015	01	0004		7765	01	20455777837	PROVESUR SRL 	11500,00	
												
Notemos que para hacer el resumen he considerado el número identificador del codigo de impuesto registrado ( es decir el que da el tipo de compra que tiene cada codigo de impuesto 												
asi tendriamos : 												
ORDEN	CONCEPTO									BASE	IMPUESTO	
1	BASE IMPONIBLE DESTINADA A  OPERACIONES GRAVADAS Y/O DE EXPORTACION									BIOGE	IGVA	
2	BASE IMPONIBLE DESTINADA A OPERACIONES GRAVADAS Y/O DE EXPORTACION Y NO GRAVADAS									BIOGENG	IGVB	
3	BASE IMPONIBLE DESTINADA A OPERACIONES NO GRAVADAS 									CNG	IGVC	
4	IMPUESTO SELECTIVO AL CONSUMO									ISC		
5	OTROS									OTROS		



	""",
	'auto_install': False,
	'demo': [],
	'data':	['wizard/account_purchase_register_wizard_view.xml','account_purchase_register_view.xml'],
	'installable': True
}
