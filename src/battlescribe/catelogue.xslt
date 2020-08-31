<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:gc="http://www.battlescribe.net/schema/gameSystemSchema">
    <xsl:key
        name="pub"
        match="gc:gameSystem/gc:publications/gc:publication"
        use="@id"/>
    <xsl:key
        name="category"
        match="gc:gameSystem/gc:categoryEntries/gc:categoryEntry"
        use="@id"/>
    <xsl:key
        name="profile"
        match="gc:gameSystem/gc:sharedProfiles/gc:profile"
        use="@id"/>
    <xsl:key
        name="rule"
        match="gc:gameSystem/gc:sharedRules/gc:rule"
        use="@id"/>
    <xsl:key
        name="selectionEntry"
        match="gc:gameSystem/gc:sharedSelectionEntries/gc:selectionEntry"
        use="@id"/>
    <xsl:key
        name="selectionEntryGroups"
        match="gc:gameSystem/gc:sharedSelectionEntryGroups/gc:selectionEntryGroup"
        use="@id"/>
    <xsl:key
        name="profileType"
        match="gc:gameSystem/gc:profileTypes/gc:profileType"
        use="@name"/>

    <xsl:template match="/">
        <html>
            <head>
                <title>40k catelogue</title>
            </head>
            <body>
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"/>
                <!-- jQuery library -->
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
                <!-- Latest compiled JavaScript -->
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>

                <h1><xsl:value-of select="gc:gameSystem/@name"/></h1>
                <xsl:value-of select="gc:gameSystem/gc:readme/text()"/>

                <h1>Publications</h1>
                <ul>
                <xsl:for-each select="gc:gameSystem/gc:publications/gc:publication">
                    <li><xsl:apply-templates select="."/></li>
                </xsl:for-each>
                </ul>

                <h1>Category Entries</h1>
                <xsl:apply-templates select="gc:gameSystem/gc:categoryEntries"/>

                <h1>Forces Entries</h1>
                <xsl:apply-templates select="gc:gameSystem/gc:forceEntries"/>


                <h1>Entry Links</h1>
                <xsl:apply-templates select="gc:gameSystem/gc:entryLinks"/>

                <h1>Shared Selection Entries</h1>
                <xsl:apply-templates select="gc:gameSystem/gc:sharedSelectionEntries"/>

                <h1>Shared Selection Entry Groups</h1>
                <xsl:apply-templates select="gc:gameSystem/gc:sharedSelectionEntryGroups"/>

                <h1>Shared Rules</h1>
                <xsl:apply-templates select="gc:gameSystem/gc:sharedRules"/>

                <h1>Shared Profiles</h1>
                <xsl:for-each select="gc:gameSystem/gc:sharedProfiles">
                    <xsl:apply-templates select="gc:profile"/>
                </xsl:for-each>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="gc:publication">
        <a>
            <xsl:attribute name="href">
                <xsl:value-of select="@publisherUrl"/>
            </xsl:attribute>
            <b><xsl:value-of select="@name"/></b>
        </a>
        &#160;
        <xsl:value-of select="@publisher"/>&#160;
        <xsl:value-of select="@publicationDate"/>
    </xsl:template>

    <xsl:template match="gc:costs">
        <xsl:for-each select="gc:cost">
            <xsl:value-of select="@name"/>:&#160;
            <xsl:value-of select="@value"/>
        </xsl:for-each>
    </xsl:template>

    <!-- has other childs too -->
    <xsl:template match="gc:categoryEntries">
        <xsl:for-each select="gc:categoryEntry">
            <span class="label label-default">
                <xsl:value-of select="@name"/>
            </span>&#160;
        </xsl:for-each>
    </xsl:template>

    <!-- Used to add a header row to a table -->
    <xsl:template match="gc:profileType">
        <tr>
            <th>Name</th>
            <xsl:for-each select="gc:characteristicTypes/gc:characteristicType">
                <th><xsl:value-of select="@name"/></th>
            </xsl:for-each>
        </tr>
    </xsl:template>

    <xsl:template match="gc:profile">
        <xsl:value-of select="@typeName"/>
        <table>
            <xsl:apply-templates select="key('profileType', @typeName)"/>
            <tr>
                <td><xsl:value-of select="@name"/></td>
                <xsl:for-each select="gc:characteristics/gc:characteristic">
                    <td><xsl:value-of select="text()"/></td>
                </xsl:for-each>
            </tr>
        </table>
    </xsl:template>

    <!-- has othere childs too -->
    <xsl:template match="gc:forceEntries">
        <xsl:for-each select="gc:forceEntry">
            <h2><xsl:value-of select="@name"/></h2>
            <!--<div style="border-style: solid;"><xsl:apply-templates select="gc:forceEntries"/></div>-->
            <xsl:apply-templates select="gc:categoryLinks"/>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="gc:sharedSelectionEntries|gc:selectionEntries">
        <xsl:for-each select="gc:selectionEntry">
            <h3><xsl:value-of select="@name"/></h3>
            <xsl:value-of select="@type"/>&#160;from&#160;
            <xsl:apply-templates select="key('pub', @publicationId)"/>
            &#160;
            <xsl:value-of select="@page"/>
            <xsl:apply-templates select="gc:costs"/>
            <xsl:for-each select="gc:profiles">
                <xsl:apply-templates select="gc:profile"/>
            </xsl:for-each>
            <xsl:for-each select="gc:rules">
                <xsl:apply-templates select="gc:rule"/>
            </xsl:for-each>
            <p><xsl:value-of select="gc:description/text()"/></p>
            <div style="border-style: solid;">
                <xsl:apply-templates select="gc:entryLinks"/>
                <xsl:apply-templates select="gc:selectionEntries"/>
                <xsl:apply-templates select="gc:selectionEntryGroups"/>
            </div>
            <xsl:apply-templates select="gc:categoryLinks"/>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:sharedSelectionEntryGroups|gc:selectionEntryGroups">
        <xsl:for-each select="gc:selectionEntryGroup">
            <h2><xsl:value-of select="@name"/></h2>
            <xsl:value-of select="@type"/>&#160;from&#160;
            <xsl:apply-templates select="key('pub', @publicationId)"/>
            &#160;
            <xsl:value-of select="@page"/>
            <xsl:apply-templates select="gc:costs"/>
            <xsl:for-each select="gc:profiles">
                <xsl:apply-templates select="gc:profile"/>
            </xsl:for-each>
            <xsl:for-each select="gc:rules">
                <xsl:apply-templates select="gc:rule"/>
            </xsl:for-each>
            <p><xsl:value-of select="gc:description/text()"/></p>
            <div style="border-style: solid;">
                <xsl:apply-templates select="gc:entryLinks"/>
                <xsl:apply-templates select="gc:selectionEntries"/>
                <xsl:apply-templates select="gc:selectionEntryGroups"/>
            </div>
            <xsl:apply-templates select="gc:categoryLinks"/>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:entryLinks">
        <xsl:for-each select="gc:entryLink">
            <h2><xsl:value-of select="@name"/></h2>
            <xsl:apply-templates select="key('pub', @publicationId)"/>
            &#160;
            <xsl:value-of select="@page"/>
            <xsl:apply-templates select="gc:costs"/>
            <xsl:apply-templates select="key(@type, @targetId)"/>
            <div style="border-style: solid;">
                <xsl:apply-templates select="gc:entryLinks"/>
                <xsl:apply-templates select="gc:selectionEntries"/>
                <xsl:apply-templates select="gc:selectionEntryGroups"/>
            </div>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:categoryLinks">
        <xsl:for-each select="gc:categoryLink">
            <xsl:value-of select="key('category', @targetId)/@name"/>:
            <xsl:value-of select="gc:constraints/gc:constraint[@type='min']/@value"/>
            -
            <xsl:value-of select="gc:constraints/gc:constraint[@type='max']/@value"/><br/>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:sharedInfoGroups|gc:infoGroups">
        <xsl:for-each select="gc:infoGroup">
            <div style="border-style: solid;">
                <xsl:apply-templates select="gc:infoGroups"/>
                <xsl:apply-templates select="gc:infoLinks"/>
            </div>
            <xsl:apply-templates select="gc:profiles"/>
            <xsl:apply-templates select="gc:rules"/>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:infoLinks">
        <xsl:for-each select="gc:infoLink">
            <h3><xsl:value-of select="@name"/></h3>
            <xsl:apply-templates select="key('pub', @publicationId)"/>
            &#160;
            <xsl:value-of select="@page"/>
            <xsl:apply-templates select="key(@type, @targetId)"/>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:rules|gc:sharedRules">
        <xsl:for-each select="gc:rule">
            <xsl:sort select="@name"/>
            <p>
                <b><xsl:value-of select="@name"/>:&#160;</b>
                <xsl:value-of select="gc:description/text()"/>
            </p>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
