<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output omit-xml-declaration="yes" method="text" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" indent="no" encoding="UTF-8" />
    <xsl:strip-space elements="*" />
    
    <xsl:template match="/icestats">
        <xsl:for-each select="source[@mount='/mount']"> <!-- CHANGE TO YOUR THE MOUNT -->
            <xsl:value-of select="@mount" /> ; <xsl:value-of select="listeners" /><xsl:text>&#13;&#10;</xsl:text>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
