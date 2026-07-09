<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="html" encoding="UTF-8" />

	<!-- Шаблон для перетворення кореневого елемента -->
	<xsl:template match="/Database">
		<html>
			<head>
				<title>Відображення даних</title>
				<style>
					table { border-collapse: collapse; width: 100%; }
					th, td { border: 1px solid black; padding: 8px; text-align: left; }
					th { background-color: #f2f2f2; }
					.highlight { font-weight: bold; color: red; }
				</style>
			</head>
			<body>
				<h2>Список Клієнтів</h2>
				<table>
					<tr>
						<th>#</th>
						<th>Customer Name</th>
						<th>Address</th>
						<th>Total Orders</th>
					</tr>
					<xsl:for-each select="Customers/Customer">
						<xsl:sort select="CustomerName" />
						<tr>
							<td>
								<xsl:number value="position()" />
							</td>
							<td>
								<xsl:value-of select="CustomerName" />
							</td>
							<td>
								<xsl:value-of select="Address" />
							</td>
							<td>
								<xsl:choose>
									<xsl:when test="count(Orders/Order) > 1">
										<span class="highlight">
											<xsl:value-of select="count(Orders/Order)" />
										</span>
									</xsl:when>
									<xsl:otherwise>
										<xsl:value-of select="count(Orders/Order)" />
									</xsl:otherwise>
								</xsl:choose>
							</td>
						</tr>
					</xsl:for-each>
				</table>

				<h2>Список Постачальників</h2>
				<ul>
					<xsl:for-each select="Suppliers/Supplier">
						<xsl:sort select="SupplierName" />
						<li>
							<xsl:value-of select="SupplierName" /> - <xsl:value-of select="PhoneNumber" />
						</li>
					</xsl:for-each>
				</ul>
			</body>
		</html>
	</xsl:template>
</xsl:stylesheet>
