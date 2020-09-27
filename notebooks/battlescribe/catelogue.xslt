<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:gc="http://www.battlescribe.net/schema/gameSystemSchema"
    xmlns:cat="http://www.battlescribe.net/schema/catalogueSchema">
    <xsl:key
        name="pub"
        match="gc:gameSystem/gc:publications/gc:publication|gc:gameSystem/cat:publications/cat:publication"
        use="@id"/>
    <xsl:key
        name="category"
        match="gc:gameSystem/gc:categoryEntries/gc:categoryEntry|gc:gameSystem/cat:categoryEntries/cat:categoryEntry"
        use="@id"/>
    <xsl:key
        name="profile"
        match="gc:gameSystem/gc:sharedProfiles/gc:profile|gc:gameSystem/cat:sharedProfiles/cat:profile"
        use="@id"/>
    <xsl:key
        name="rule"
        match="gc:gameSystem/gc:sharedRules/gc:rule|gc:gameSystem/cat:sharedRules/cat:rule"
        use="@id"/>
    <xsl:key
        name="selectionEntry"
        match="gc:gameSystem/gc:sharedSelectionEntries/gc:selectionEntry|gc:gameSystem/cat:sharedSelectionEntries/cat:selectionEntry"
        use="@id"/>
    <xsl:key
        name="selectionEntryGroup"
        match="gc:gameSystem/gc:sharedSelectionEntryGroups/gc:selectionEntryGroup|gc:gameSystem/cat:sharedSelectionEntryGroups/cat:selectionEntryGroup"
        use="@id"/>
    <xsl:key
        name="profileType"
        match="gc:gameSystem/gc:profileTypes/gc:profileType|gc:gameSystem/cat:profileTypes/cat:profileType"
        use="@name"/>
    <xsl:key
        name="allIds"
        match="//*[@id]"
        use="@id"/>
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

                <!--<h1><xsl:value-of select="gc:gameSystem/@name"/></h1>
                <xsl:value-of select="gc:gameSystem/gc:readme/text()"/>-->

                <h1>Publications</h1>
                <ul>
                <xsl:for-each select="//cat:publication">
                    <li><xsl:apply-templates select="."/></li>
                </xsl:for-each>
                </ul>

                <h1>Index</h1>
                <ul>
                    <xsl:for-each select="gc:gameSystem/cat:entryLinks/cat:entryLink">
                    <li><a>
                        <xsl:attribute name="href">
                            #<xsl:value-of select="@id"/>
                        </xsl:attribute>
                        <xsl:value-of select="key(@type, @targetId)/@name"/>
                    </a></li>
                    </xsl:for-each>
                </ul>

                <xsl:if test="gc:gameSystem/cat:forceEntries">
                    <h1>Forces Entries</h1>
                    <xsl:apply-templates select="gc:gameSystem/gc:forceEntries|gc:gameSystem/cat:forceEntries"/>
                </xsl:if>

                <h1>Entries</h1>
                <xsl:apply-templates select="gc:gameSystem/cat:entryLinks"/>

            </body>
        </html>
    </xsl:template>

    <!-- named templates-->
    <xsl:template name="commentable">
        <xsl:if test="gc:comment|cat:comment">
            <p>
                <b>Comment:</b>
                <xsl:value-of select="gc:comment/text()|cat:comment/text()"/>
            </p>
        </xsl:if>
    </xsl:template>
    <xsl:template name="publicationRef">
        <xsl:if test=" @publicationId">
            Publication:&#160;
            <xsl:apply-templates select="key('pub', @publicationId)"/>
            &#160;
            <xsl:if test="@page">
                p<xsl:value-of select="@page"/>
            </xsl:if>
        </xsl:if>
    </xsl:template>
    <xsl:template name="entryBase">
        <h2><a>
            <xsl:attribute name="id">
                <xsl:value-of select="@id"/>
            </xsl:attribute>
            <xsl:value-of select="@name"/>
        </a></h2>
        <xsl:call-template name="commentable"/>
        <xsl:call-template name="publicationRef"/>
        <xsl:apply-templates select="gc:modifiers|cat:modifiers"/>
        <xsl:apply-templates select="gc:modifierGroups|cat:modifierGroups"/>
    </xsl:template>
    <xsl:template name="containerEntryBase">
        <xsl:call-template name="entryBase"/>
        <xsl:apply-templates select="gc:constraints|cat:constraints"/>
        <xsl:call-template name="infoNodeGroup"/>
    </xsl:template>
    <xsl:template name="primaryCategory">
        <h1>
            <span class="badge badge-secondary" style="margin: 2px;">
                <xsl:value-of
                select="key('category', gc:categoryLinks/gc:categoryLink[@primary='true']/@targetId|cat:categoryLinks/cat:categoryLink[@primary='true']/@targetId)/@name"/>
            </span>
        </h1>
    </xsl:template>
    <xsl:template name="selectionEntryBase">
        <xsl:call-template name="primaryCategory"/>
        <xsl:call-template name="containerEntryBase"/>
        <xsl:if test="gc:selectionEntries|cat:selectionEntries|gc:selectionEntryGroups|cat:selectionEntryGroups|gc:entryLinks|cat:entryLinks">
            <xsl:apply-templates select="gc:selectionEntries|cat:selectionEntries"/>
            <xsl:apply-templates select="gc:selectionEntryGroups|cat:selectionEntryGroups"/>
            <xsl:apply-templates select="gc:entryLinks|cat:entryLinks"/>
        </xsl:if>
        <xsl:if test="gc:categoryLinks|cat:categoryLinks">
            <xsl:apply-templates select="gc:categoryLinks|cat:categoryLinks"/>
        </xsl:if>
    </xsl:template>
    <xsl:template name="infoNodeGroup">
        <xsl:apply-templates select="gc:profiles|cat:profiles"/>
        <xsl:apply-templates select="gc:rules|cat:rules"/>
        <xsl:apply-templates select="gc:infoGroups|cat:infoGroups"/>
        <xsl:apply-templates select="gc:infoLinks|cat:infoLinks"/>
    </xsl:template>
    <xsl:template name="infoGroup">
        <xsl:call-template name="entryBase"/>
        <xsl:call-template name="infoNodeGroup"/>
    </xsl:template>

    <xsl:template match="gc:publication|cat:publication">
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

    <xsl:template match="gc:costs|cat:costs">
        <xsl:for-each select="gc:cost|cat:cost">
            <xsl:if test="number(@value) > 0.0">
                <span class="label label-default" style="margin: 2px;">
                    <xsl:value-of select="@name"/>:&#160;
                    <xsl:value-of select="@value"/>
                </span>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="gc:categoryEntries|cat:categoryEntries">
        <xsl:for-each select="gc:categoryEntry|cat:categoryEntry">
            <xsl:apply-templates select="."/>&#160;
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:categoryEntry|cat:categoryEntry">
        <!--<div style="border-style: solid; padding: 2px; margin: 2px;">-->
            <span class="label label-default" style="margin: 2px;">
                <xsl:value-of select="@name"/>
            </span>
            <!-- took out as seems to be empty
                <xsl:call-template name="containerEntryBase"/>-->
        <!--</div>-->
    </xsl:template>

    <!-- Used to add a header row to a table -->
    <xsl:template match="gc:profileType|cat:profileType">
        <tr>
            <th><xsl:value-of select="@name"/> Name</th>
            <xsl:for-each select="gc:characteristicTypes/gc:characteristicType|cat:characteristicTypes/cat:characteristicType">
                <th><xsl:value-of select="@name"/></th>
            </xsl:for-each>
        </tr>
    </xsl:template>

    <xsl:template match="gc:profile|cat:profile">
        <!--<xsl:call-template name="entryBase"/>-->
        <table class="table">
            <xsl:apply-templates select="key('profileType', @typeName)"/>
            <tr>
                <td><xsl:value-of select="@name"/></td>
                <xsl:for-each select="gc:characteristics/gc:characteristic|cat:characteristics/cat:characteristic">
                    <td><xsl:value-of select="text()"/></td>
                </xsl:for-each>
            </tr>
        </table>
    </xsl:template>

    <xsl:template match="gc:forceEntries|cat:forceEntries">
        <xsl:for-each select="gc:forceEntry|cat:forceEntry">
            <div style="border-style: solid; padding: 2px; margin: 2px;">
                <!--<xsl:call-template name="containerEntryBase"/>-->
                Child Forces: <xsl:apply-templates select="gc:forceEntries|cat:forceEntries"/>
                Tags: <xsl:apply-templates select="gc:categoryLinks|cat:categoryLinks"/>
            </div>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="gc:sharedSelectionEntries|gc:selectionEntries|cat:sharedSelectionEntries|cat:selectionEntries">
        <xsl:for-each select="gc:selectionEntry|cat:selectionEntry">
            <div style="border-style: solid; padding: 2px; margin: 2px;">
                <b>type: </b><xsl:value-of select="@type"/>
                <xsl:call-template name="selectionEntryBase"/>
                <b>costs: </b><xsl:apply-templates select="gc:costs|cat:costs"/>
            </div>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:sharedSelectionEntryGroups|gc:selectionEntryGroups|cat:sharedSelectionEntryGroups|cat:selectionEntryGroups">
        <xsl:for-each select="gc:selectionEntryGroup|cat:selectionEntryGroup">
            <div style="border-style: solid; padding: 2px; margin: 2px;">
                <xsl:call-template name="selectionEntryBase"/>
                <a>
                    <xsl:attribute name="href">
                        <xsl:value-of select="@defaultSelectionEntryId"/>
                    </xsl:attribute>
                    <xsl:value-of select="key('allIds', @defaultSelectionEntryId)/@name"/>
                </a>
            </div>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:entryLinks|cat:entryLinks">
        <xsl:for-each select="gc:entryLink|cat:entryLink">
            <div style="border-style: solid; padding: 2px; margin: 2px;">
                <xsl:call-template name="selectionEntryBase"/>
                <xsl:apply-templates select="gc:costs|cat:costs"/>
                <xsl:apply-templates select="key(@type, @targetId)"/>
                <xsl:apply-templates select="gc:entryLinks|cat:entryLinks"/>
            </div>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:categoryLinks|cat:categoryLinks">
        <xsl:for-each select="gc:categoryLink|cat:categoryLink">
            <!--<xsl:call-template name="containerEntryBase"/>-->
            <xsl:apply-templates select="key('category', @targetId)"/>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:sharedInfoGroups|gc:infoGroups|cat:sharedInfoGroups|cat:infoGroups">
        <xsl:for-each select="gc:infoGroup|cat:infoGroup">
            <div style="border-style: solid; padding: 2px; margin: 2px;">
                <xsl:call-template name="infoGroup"/>
            </div>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:infoLinks|cat:infoLinks">
        <xsl:for-each select="gc:infoLink|cat:infoLink">
            <div style="border-style: solid; padding: 2px; margin: 2px;">
                <xsl:call-template name="entryBase"/>
                <xsl:apply-templates select="key(@type, @targetId)"/>
            </div>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:rules|gc:sharedRules|cat:rules|cat:sharedRules">
        <xsl:for-each select="gc:rule|cat:rule">
            <xsl:call-template name="entryBase"/>
            <p>
                <b><xsl:value-of select="@name"/>:&#160;</b>
                <xsl:value-of select="gc:description/text()|cat:description/text()"/>
            </p>
        </xsl:for-each>
    </xsl:template>
    <xsl:template name="queryBase">
        <xsl:value-of select="@field"/>
        =<xsl:choose>
            <xsl:when test="string(number(myNode)) != 'NaN'">
                <xsl:value-of select="round(@value)"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="@value"/>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:if test="@percentValue = 'true'">%</xsl:if>
        &#160;in&#160;<xsl:value-of select="@scope"/>
        &#160;<xsl:if test="@shared = 'true'">shared</xsl:if>
        &#160;<xsl:if test="@includeChildSelections = 'true'">includechildselection</xsl:if>
        &#160;<xsl:if test="@includeChildForce = 'true'">includechildforce</xsl:if>
        <br/>
    </xsl:template>
    <xsl:template match="gc:constraints|cat:constraints">
        <xsl:for-each select="gc:constraint|cat:constraint">
                <a>
                    <xsl:attribute name="href">
                        #<xsl:value-of select="@id"/>
                    </xsl:attribute>
                    <xsl:text>link</xsl:text>
                </a>
                type: <xsl:value-of select="@type"/>
                &#160;<xsl:call-template name="queryBase"/>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="gc:conditions|cat:conditions">
        <div style="border-style: solid; padding: 2px; margin: 2px;">
            <xsl:for-each select="gc:condition|cat:condition">
                <a>
                    <xsl:attribute name="href">
                        #<xsl:value-of select="@childId"/>
                    </xsl:attribute>
                    <xsl:text>Child</xsl:text>
                </a>
                type: <xsl:value-of select="@type"/>
                &#160;<xsl:call-template name="queryBase"/>
            </xsl:for-each>
        </div>
    </xsl:template>
        <xsl:template match="gc:repeats|cat:repeats">
        <div style="border-style: solid; padding: 2px; margin: 2px;">
            <xsl:for-each select="gc:repeat|cat:repeat">
                type: <xsl:value-of select="@type"/>
                <a>child<xsl:value-of select="@childId"/></a>
                &#160;<xsl:call-template name="queryBase"/>
                &#160;repeats: <xsl:value-of select="@includeChildForce"/>
                &#160;roundup: <xsl:value-of select="@roundUp"/>
                <br/>
            </xsl:for-each>
        </div>
    </xsl:template>
    <xsl:template match="gc:conditionGroups|cat:conditionGroups">
        <div style="border-style: solid; padding: 2px; margin: 2px;">
            <xsl:apply-templates select="gc:conditions|cat:conditions"/>
            <xsl:apply-templates select="gc:conditionGroups|cat:conditionGroups"/>
        </div>
    </xsl:template>
    <xsl:template match="gc:modifiers|cat:modifiers">
        <xsl:for-each select="gc:modifier|cat:modifier">
            <div style="border-style: solid; padding: 2px; margin: 2px;">
                <xsl:if test="gc:conditions|gc:conditionGroups|cat:conditions|cat:conditionGroups">
                    if&#160;<xsl:apply-templates select="gc:conditions|cat:conditions"/>
                    <xsl:apply-templates select="gc:conditionGroups|cat:conditionGroups"/>
                </xsl:if>
                <xsl:value-of select="@type"/>
                &#160;<xsl:value-of select="@field"/>
                =<xsl:choose>
                    <xsl:when test="string(number(myNode)) != 'NaN'">
                        <xsl:value-of select="round(@value)"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="@value"/>
                    </xsl:otherwise>
                </xsl:choose>
                <xsl:apply-templates select="gc:repeats|cat:repeats"/>
            </div>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
