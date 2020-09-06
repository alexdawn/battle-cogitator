<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:gc="http://www.battlescribe.net/schema/gameSystemSchema"
    xmlns:cat="http://www.battlescribe.net/schema/catalogueSchema">
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
                <!--
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
                -->
            </body>
        </html>
    </xsl:template>

    <!-- named templates-->
    <xsl:template name="commentable">
        <xsl:if test="comment">
            <p>Comment:<xsl:value-of select="comment/text()"/></p>
        </xsl:if>
    </xsl:template>
    <xsl:template name="publicationRef">
        <xsl:if test=" @publicationId">
            Publication:&#160;
            <xsl:apply-templates select="key('pub', @publicationId)"/>
            &#160;
            <xsl:value-of select="@page"/>
        </xsl:if>
    </xsl:template>
    <xsl:template name="entryBase">
        <h2>
            <xsl:attribute name="id">
                <xsl:value-of select="@id"/>
            </xsl:attribute>
            <xsl:value-of select="@name"/>
        </h2>
        <xsl:call-template name="commentable"/>
        <xsl:call-template name="publicationRef"/>
        <xsl:apply-templates select="gc:modifiers"/>
        <xsl:apply-templates select="gc:modifierGroups"/>
    </xsl:template>
    <xsl:template name="containerEntryBase">
        <xsl:call-template name="entryBase"/>
        <xsl:apply-templates select="gc:constraints"/>
        <xsl:call-template name="infoNodeGroup"/>
    </xsl:template>
    <xsl:template name="primaryCategory">
        <h1>
            <span class="badge badge-secondary">
                <xsl:value-of select="key('category', gc:categoryLinks/gc:categoryLink[@primary='true']/@targetId)/@name"/>
            </span>
        </h1>
    </xsl:template>
    <xsl:template name="selectionEntryBase">
        <xsl:call-template name="primaryCategory"/>
        <xsl:call-template name="containerEntryBase"/>
        Category Links:<xsl:apply-templates select="gc:categoryLinks"/>
        Selection Entries:<xsl:apply-templates select="gc:selectionEntries"/>
        Selection Entry Groups:<xsl:apply-templates select="gc:selectionEntryGroups"/>
        Entry Links:<xsl:apply-templates select="gc:entryLinks"/>
    </xsl:template>
    <xsl:template name="infoNodeGroup">
        Profiles:<xsl:apply-templates select="gc:profiles"/>
        Rules:<xsl:apply-templates select="gc:rules"/>
        Info Groups:<xsl:apply-templates select="gc:infoGroups"/>
        Info Links:<xsl:apply-templates select="gc:infoLinks"/>
    </xsl:template>
    <xsl:template name="infoGroup">
        <xsl:call-template name="entryBase"/>
        <xsl:call-template name="infoNodeGroup"/>
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
            <xsl:if test="number(@value) > 0.0">
                <span class="label label-default">
                    <xsl:value-of select="@name"/>:&#160;
                    <xsl:value-of select="@value"/>
                </span>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="gc:categoryEntries">
        <xsl:for-each select="gc:categoryEntry">
            <xsl:apply-templates select="."/>&#160;
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:categoryEntry">
        <!--<div style="border-style: solid; margin: 2px;">-->
            <span class="label label-default">
                <xsl:value-of select="@name"/>
            </span>
            <!-- took out as seems to be empty
                <xsl:call-template name="containerEntryBase"/>-->
        <!--</div>-->
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
        <xsl:call-template name="entryBase"/>
        profile Type: <xsl:value-of select="@typeName"/>
        <table class="table">
            <xsl:apply-templates select="key('profileType', @typeName)"/>
            <tr>
                <td><xsl:value-of select="@name"/></td>
                <xsl:for-each select="gc:characteristics/gc:characteristic">
                    <td><xsl:value-of select="text()"/></td>
                </xsl:for-each>
            </tr>
        </table>
    </xsl:template>

    <xsl:template match="gc:forceEntries">
        <xsl:for-each select="gc:forceEntry">
            <div style="border-style: solid; margin: 2px;">
                <!--<xsl:call-template name="containerEntryBase"/>-->
                Child Forces: <xsl:apply-templates select="gc:forceEntries"/>
                Tags: <xsl:apply-templates select="gc:categoryLinks"/>
            </div>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="gc:sharedSelectionEntries|gc:selectionEntries">
        <xsl:for-each select="gc:selectionEntry">
            <div style="border-style: solid; margin: 2px;">
                <xsl:call-template name="containerEntryBase"/>
                type:<xsl:value-of select="@type"/>
                costs:<xsl:apply-templates select="gc:costs"/>
            </div>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:sharedSelectionEntryGroups|gc:selectionEntryGroups">
        <xsl:for-each select="gc:selectionEntryGroup">
            <div style="border-style: solid; margin: 2px;">
                <xsl:call-template name="selectionEntryBase"/>
                Default Selection: <xsl:value-of select="@defaultSelectionEntryId"/>
            </div>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:entryLinks">
        <xsl:for-each select="gc:entryLink">
            <div style="border-style: solid; margin: 2px;">
                <xsl:call-template name="selectionEntryBase"/>
                costs:<xsl:apply-templates select="gc:costs"/>
                link:<xsl:apply-templates select="key(@type, @targetId)"/>
                entry links:<xsl:apply-templates select="gc:entryLinks"/>
            </div>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:categoryLinks">
        <xsl:for-each select="gc:categoryLink">
            <!--<xsl:call-template name="containerEntryBase"/>-->
            <xsl:apply-templates select="key('category', @targetId)"/>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:sharedInfoGroups|gc:infoGroups">
        <xsl:for-each select="gc:infoGroup">
            <div style="border-style: solid; margin: 2px;">
                <xsl:call-template name="infoGroup"/>
            </div>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:infoLinks">
        <xsl:for-each select="gc:infoLink">
            <div style="border-style: solid; margin: 2px;">
                <xsl:call-template name="entryBase"/>
                <xsl:apply-templates select="key(@type, @targetId)"/>
            </div>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:rules|gc:sharedRules">
        <xsl:for-each select="gc:rule">
            <xsl:call-template name="entryBase"/>
            <p>
                <b><xsl:value-of select="@name"/>:&#160;</b>
                <xsl:value-of select="gc:description/text()"/>
            </p>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:constraints">
        <xsl:for-each select="gc:constraint">
                id: <xsl:value-of select="@id"/>
                type: <xsl:value-of select="@type"/>
                field: <xsl:value-of select="@field"/>
                scope: <xsl:value-of select="@scope"/>
                value: <xsl:value-of select="@value"/>
                <xsl:if test="@percentValue = 'true'">%</xsl:if>
                shared: <xsl:value-of select="@shared"/>
                includechildselection: <xsl:value-of select="@includeChildSelections"/>
                includechildforce: <xsl:value-of select="@includeChildForce"/>
                <br/>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:conditions">
        <div style="border-style: solid; margin: 2px;">
            <xsl:for-each select="gc:condition">
                type: <xsl:value-of select="@type"/>
                child: <xsl:value-of select="@childId"/>
                field: <xsl:value-of select="@field"/>
                scope: <xsl:value-of select="@scope"/>
                value: <xsl:value-of select="@value"/>
                <xsl:if test="@percentValue = 'true'">%</xsl:if>
                shared: <xsl:value-of select="@shared"/>
                includechildselection: <xsl:value-of select="@includeChildSelections"/>
                includechildforce: <xsl:value-of select="@includeChildForce"/>
                <br/>
            </xsl:for-each>
        </div>
    </xsl:template>
        <xsl:template match="gc:repeats">
        <div style="border-style: solid; margin: 2px;">
            <xsl:for-each select="gc:repeat">
                type: <xsl:value-of select="@type"/>
                <a>child<xsl:value-of select="@childId"/></a>
                field: <xsl:value-of select="@field"/>
                scope: <xsl:value-of select="@scope"/>
                value: <xsl:value-of select="@value"/>
                <xsl:if test="@percentValue = 'true'">%</xsl:if>
                shared: <xsl:value-of select="@shared"/>
                includechildselection: <xsl:value-of select="@includeChildSelections"/>
                includechildforce: <xsl:value-of select="@includeChildForce"/>
                repeats: <xsl:value-of select="@includeChildForce"/>
                roundup: <xsl:value-of select="@roundUp"/>
                <br/>
            </xsl:for-each>
        </div>
    </xsl:template>
    <xsl:template match="gc:conditionGroups">
        <xsl:for-each select="gc:conditionGroup">
            <div style="border-style: solid; margin: 2px;">
                <xsl:apply-templates select="gc:conditions"/>
                <xsl:apply-templates select="gc:conditionGroups"/>
            </div>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:modifiers">
        <xsl:for-each select="gc:modifier">
            <div style="border-style: solid; margin: 2px;">
                type:<xsl:value-of select="@type"/>
                field:<xsl:value-of select="@field"/>
                value:<xsl:value-of select="@value"/>
                repeats:<xsl:apply-templates select="gc:repeats"/>
                conditions:<xsl:apply-templates select="gc:conditions"/>
                conditions group:<xsl:apply-templates select="gc:conditionGroups"/>
            </div>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
