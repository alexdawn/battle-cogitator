<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:gc="http://www.battlescribe.net/schema/gameSystemSchema"
    xmlns:cat="http://www.battlescribe.net/schema/catalogueSchema">
    <xsl:output method="text"/>
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
        <xsl:text>{</xsl:text>
        <xsl:apply-templates select="gc:gameSystem/cat:entryLinks"/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <!-- named templates-->
    <xsl:template name="commentable">
        <xsl:text>"comment": "</xsl:text>
        <xsl:value-of select="gc:comment/text()|cat:comment/text()"/>
        <xsl:text>",&#xd;</xsl:text>
    </xsl:template>

    <xsl:template name="entryBase">
        <xsl:text>"id": "</xsl:text>
        <xsl:value-of select="@id"/>
        <xsl:text>",&#xd;</xsl:text>
        <xsl:text>"name": "</xsl:text>
        <xsl:value-of select="@name"/>
        <xsl:text>",&#xd;</xsl:text>
        <xsl:call-template name="commentable"/>
        <xsl:apply-templates select="gc:modifiers|cat:modifiers"/>
        <xsl:apply-templates select="gc:modifierGroups|cat:modifierGroups"/>
    </xsl:template>

    <xsl:template name="containerEntryBase">
        <xsl:call-template name="entryBase"/>
        <xsl:text>,&#xd;</xsl:text>
        <xsl:apply-templates select="gc:constraints|cat:constraints"/>
        <xsl:text>,&#xd;</xsl:text>
        <xsl:call-template name="infoNodeGroup"/>
    </xsl:template>

    <xsl:template name="primaryCategory">
        <xsl:text>"primary_category": "</xsl:text>
        <xsl:value-of select="key(
            'category',
            gc:categoryLinks/gc:categoryLink[@primary='true']/@targetId|
            cat:categoryLinks/cat:categoryLink[@primary='true']/@targetId)/@name"/>
        <xsl:text>",&#xd;</xsl:text>
    </xsl:template>

    <xsl:template name="selectionEntryBase">
        <xsl:call-template name="primaryCategory"/>
        <xsl:call-template name="containerEntryBase"/>
        <xsl:apply-templates select="gc:selectionEntries|cat:selectionEntries"/>
        <xsl:text>,&#xd;</xsl:text>
        <xsl:apply-templates select="gc:selectionEntryGroups|cat:selectionEntryGroups"/>
        <xsl:text>,&#xd;</xsl:text>
        <xsl:apply-templates select="gc:entryLinks|cat:entryLinks"/>
        <xsl:text>,&#xd;</xsl:text>
        <xsl:apply-templates select="gc:categoryLinks|cat:categoryLinks"/>
    </xsl:template>

    <xsl:template name="infoNodeGroup">
        <xsl:apply-templates select="gc:profiles|cat:profiles"/>
        <xsl:text>,&#xd;</xsl:text>
        <xsl:apply-templates select="gc:rules|cat:rules"/>
        <xsl:text>,&#xd;</xsl:text>
        <xsl:apply-templates select="gc:infoGroups|cat:infoGroups"/>
        <xsl:text>,&#xd;</xsl:text>
        <xsl:apply-templates select="gc:infoLinks|cat:infoLinks"/>
    </xsl:template>

    <xsl:template name="infoGroup">
        <xsl:call-template name="entryBase"/>
        <xsl:text>,&#xd;</xsl:text>
        <xsl:call-template name="infoNodeGroup"/>
    </xsl:template>

    <xsl:template match="gc:cost|cat:cost">
        <xsl:text>"</xsl:text>
        <xsl:value-of select="normalize-space(@name)"/>
        <xsl:text>": "</xsl:text>
        <xsl:value-of select="@value"/>
        <xsl:text>"&#xd;</xsl:text>
    </xsl:template>

    <xsl:template match="gc:costs|cat:costs">
        <xsl:for-each select="(gc:cost|cat:cost)[@value > 0]">
            <xsl:apply-templates select="."/>
            <xsl:if test="position() != last()">
                <xsl:text>,&#xD;</xsl:text>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="gc:categoryEntries|cat:categoryEntries">
        <xsl:text>"category_entries": [</xsl:text>
        <xsl:for-each select="gc:categoryEntry|cat:categoryEntry">
            <xsl:apply-templates select="."/>&#xD;
        </xsl:for-each>
        <xsl:text>]&#xd;</xsl:text>
    </xsl:template>

    <xsl:template match="gc:categoryEntry|cat:categoryEntry">
        <xsl:text>"</xsl:text>
        <xsl:value-of select="@name"/>
        <xsl:text>"</xsl:text>
        <xsl:if test="position() != last()">
            <xsl:text>,&#xD;</xsl:text>
        </xsl:if>
    </xsl:template>

    <xsl:template match="gc:profiles|cat:profiles">
        <xsl:text>"profiles": [</xsl:text>
        <xsl:for-each select="gc:profile|cat:profile">
            <xsl:text>{&#xD;</xsl:text>
            <xsl:apply-templates select="."/>
            <xsl:text>}</xsl:text>
            <xsl:if test="position() != last()">
                <xsl:text>,&#xD;</xsl:text>
            </xsl:if>
        </xsl:for-each>
        <xsl:text>]</xsl:text>
    </xsl:template>

    <xsl:template match="gc:profile|cat:profile">
        <xsl:text>"type": "profile", "profile_type": "</xsl:text>
        <xsl:value-of select="@typeName"/>
        <xsl:text>",&#xd;</xsl:text>
        <xsl:text>"name": "</xsl:text>
        <xsl:value-of select="@name"/>
        <xsl:text>",&#xd;</xsl:text>
        <xsl:for-each select="gc:characteristics/gc:characteristic|cat:characteristics/cat:characteristic">
            <xsl:text>"</xsl:text>
            <xsl:value-of select="@name"/>
            <xsl:text>": "</xsl:text>
            <xsl:value-of select="text()"/>
            <xsl:text>"</xsl:text>
            <xsl:if test="position() != last()">
                <xsl:text>,&#xD;</xsl:text>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="gc:selectionEntry|cat:selectionEntry">
        <xsl:text>"type": "</xsl:text>
        <xsl:value-of select="@type"/>
        <xsl:text>",&#xd;</xsl:text>
        <xsl:call-template name="selectionEntryBase"/>
        <xsl:text>"costs": {</xsl:text>
        <xsl:apply-templates select="gc:costs|cat:costs"/>
        <xsl:text>}&#xd;</xsl:text>
    </xsl:template>

    <xsl:template match="gc:sharedSelectionEntries|gc:selectionEntries|cat:sharedSelectionEntries|cat:selectionEntries">
        <xsl:text>"selection_entries": [</xsl:text>
        <xsl:for-each select="gc:selectionEntry|cat:selectionEntry">
            <xsl:text>{</xsl:text>
                <xsl:apply-templates select="."/>
            <xsl:text>}&#xd;</xsl:text>
            <xsl:if test="position() != last()">
                <xsl:text>,&#xD;</xsl:text>
            </xsl:if>
        </xsl:for-each>
        <xsl:text>]&#xd;</xsl:text>
    </xsl:template>

    <xsl:template match="gc:sharedSelectionEntryGroups|gc:selectionEntryGroups|cat:sharedSelectionEntryGroups|cat:selectionEntryGroups">
        <xsl:text>"seletion_entry_groups": [</xsl:text>
        <xsl:for-each select="gc:selectionEntryGroup|cat:selectionEntryGroup">
            <xsl:text>{</xsl:text>
            <xsl:call-template name="selectionEntryBase"/>
            <xsl:text>"default_selection": "</xsl:text>
            <xsl:value-of select="@defaultSelectionEntryId"/>
            <xsl:text>"}</xsl:text>
            <xsl:if test="position() != last()">
                <xsl:text>,&#xD;</xsl:text>
            </xsl:if>
        </xsl:for-each>
        <xsl:text>]&#xd;</xsl:text>
    </xsl:template>

    <xsl:template match="gc:entryLinks|cat:entryLinks">
        <xsl:text>"entry_links": [</xsl:text>
        <xsl:for-each select="gc:entryLink|cat:entryLink">
            <xsl:text>{</xsl:text>
            <xsl:call-template name="selectionEntryBase"/>
            <xsl:text>"costs": {</xsl:text>
            <xsl:apply-templates select="gc:costs|cat:costs"/>
            <xsl:text>},&#xd;</xsl:text>
            <xsl:text>"target_type": "</xsl:text>
            <xsl:apply-templates select="@type"/>
            <xsl:text>",&#xd;</xsl:text>
            <xsl:apply-templates select="gc:entryLinks|cat:entryLinks"/>
            <xsl:if test="gc:entryLinks|cat:entryLinks">
                <xsl:text>,&#xd;</xsl:text>
            </xsl:if>
            <xsl:text>"link_target": {</xsl:text>
            <xsl:apply-templates select="key(@type, @targetId)"/>
            <xsl:text>}</xsl:text>
            <xsl:text>}</xsl:text>
            <xsl:if test="position() != last()">
                <xsl:text>,&#xD;</xsl:text>
            </xsl:if>
        </xsl:for-each>
        <xsl:text>]&#xd;</xsl:text>
    </xsl:template>

    <xsl:template match="gc:categoryLinks|cat:categoryLinks">
        <xsl:text>"category_links": [</xsl:text>
        <xsl:for-each select="gc:categoryLink|cat:categoryLink">
            <xsl:apply-templates select="key('category', @targetId)"/>
            <xsl:if test="position() != last()">
                <xsl:text>,&#xD;</xsl:text>
            </xsl:if>
        </xsl:for-each>
        <xsl:text>]&#xd;</xsl:text>
    </xsl:template>

    <xsl:template match="gc:sharedInfoGroups|gc:infoGroups|cat:sharedInfoGroups|cat:infoGroups">
        <xsl:text>"info_group": [</xsl:text>
        <xsl:for-each select="gc:infoGroup|cat:infoGroup">
            <xsl:text>{</xsl:text>
            <xsl:call-template name="infoGroup"/>
            <xsl:text>}</xsl:text>
            <xsl:if test="position() != last()">
                <xsl:text>,&#xD;</xsl:text>
            </xsl:if>
        </xsl:for-each>
        <xsl:text>]&#xd;</xsl:text>
    </xsl:template>

    <xsl:template match="gc:infoLinks|cat:infoLinks">
        <xsl:text>"info_links": [&#xd;</xsl:text>
        <xsl:for-each select="gc:infoLink|cat:infoLink">
            <xsl:text>{&#xd;</xsl:text>
            <xsl:text>"type": "info_link",&#xd;</xsl:text>
            <xsl:text>"target_type": "</xsl:text>
            <xsl:value-of select="@type"/>
            <xsl:text>",&#xd;</xsl:text>
            <xsl:call-template name="entryBase"/>
            <xsl:text>"info_target": {</xsl:text>
            <xsl:apply-templates select="key(@type, @targetId)"/>
            <xsl:text>}}</xsl:text>
            <xsl:if test="position() != last()">
                <xsl:text>,&#xD;</xsl:text>
            </xsl:if>
        </xsl:for-each>
        <xsl:text>]&#xd;</xsl:text>
    </xsl:template>

    <xsl:template match="gc:rule|cat:rule">
        <xsl:call-template name="entryBase"/>
        <xsl:text>"rule_name": "</xsl:text>
        <xsl:value-of select="@name"/>
        <xsl:text>",</xsl:text>
        <xsl:text>"description": "</xsl:text>
        <xsl:value-of select="gc:description/text()|cat:description/text()"/>
        <xsl:text>"&#xd;</xsl:text>
    </xsl:template>

    <xsl:template match="gc:rules|gc:sharedRules|cat:rules|cat:sharedRules">
        <xsl:text>"rules": [&#xd;</xsl:text>
            <xsl:for-each select="gc:rule|cat:rule">
                <xsl:text>{</xsl:text>
                <xsl:apply-templates select="."/>
                <xsl:text>}</xsl:text>
                <xsl:if test="position() != last()">
                    <xsl:text>,&#xD;</xsl:text>
                </xsl:if>
            </xsl:for-each>
        <xsl:text>]&#xd;</xsl:text>
    </xsl:template>

    <xsl:template name="queryBase">
        <xsl:text>"field": "</xsl:text>
        <xsl:value-of select="@field"/>
        <xsl:text>",&#xd;</xsl:text>
        <xsl:text>"value": "</xsl:text>
        <xsl:choose>
            <xsl:when test="string(number(myNode)) != 'NaN'">
                <xsl:value-of select="round(@value)"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="@value"/>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:if test="@percentValue = 'true'">
            <xsl:text>%</xsl:text>
        </xsl:if>
        <xsl:text>",&#xd;</xsl:text>
        <xsl:text>"scope": "</xsl:text>
        <xsl:value-of select="@scope"/>
        <xsl:text>",&#xd;</xsl:text>
        <xsl:text>"shared": </xsl:text>
        <xsl:value-of select="@shared"/>
        <xsl:text>,&#xd;</xsl:text>
        <xsl:text>"includechildselection": "</xsl:text>
        <xsl:value-of select="@includeChildSelections"/>
        <xsl:text>",&#xd;</xsl:text>
        <xsl:text>"includechildforce": "</xsl:text>
        <xsl:value-of select="@includeChildForce"/>
        <xsl:text>"&#xd;</xsl:text>
    </xsl:template>

    <xsl:template match="gc:constraints|cat:constraints">
        <xsl:text>"constraints": [&#xd;</xsl:text>
        <!--<xsl:for-each select="gc:constraint|cat:constraint">
            <xsl:text>{&#xd;</xsl:text>
            <xsl:text>"id": "</xsl:text>
            <xsl:value-of select="@id"/>
            <xsl:text>",&#xd;</xsl:text>
            <xsl:text>"type": "</xsl:text>
            <xsl:value-of select="@type"/>
            <xsl:text>",&#xd;</xsl:text>
            <xsl:call-template name="queryBase"/>
            <xsl:text>}</xsl:text>
            <xsl:if test="position() != last()">
                <xsl:text>,&#xD;</xsl:text>
            </xsl:if>
        </xsl:for-each>-->
        <xsl:text>]&#xd;</xsl:text>
    </xsl:template>

    <xsl:template match="gc:conditions|cat:conditions">
        <xsl:text>"conditions": [&#xd;</xsl:text>
        <!--<xsl:for-each select="gc:condition|cat:condition">
            <xsl:text>{&#xd;</xsl:text>
            <xsl:text>"child_id": "</xsl:text>
            <xsl:value-of select="@childId"/>
            <xsl:text>",&#xd;</xsl:text>
            <xsl:text>"type": "</xsl:text>
            <xsl:value-of select="@type"/>
            <xsl:text>",&#xd;</xsl:text>
            <xsl:call-template name="queryBase"/>
            <xsl:text>}</xsl:text>
            <xsl:if test="position() != last()">
                <xsl:text>,&#xD;</xsl:text>
            </xsl:if>
        </xsl:for-each>-->
        <xsl:text>]&#xd;</xsl:text>
    </xsl:template>

    <xsl:template match="gc:repeats|cat:repeats">
        <!--<xsl:for-each select="gc:repeat|cat:repeat">
            <xsl:text>{&#xd;</xsl:text>
            <xsl:text>"type": "</xsl:text>
            <xsl:value-of select="@type"/>
            <xsl:text>",&#xd;</xsl:text>
            <xsl:text>"child_id": "</xsl:text>
            <xsl:value-of select="@childId"/>
            <xsl:text>",&#xd;</xsl:text>
            <xsl:call-template name="queryBase"/>
            <xsl:text>"repeats": "</xsl:text>
            <xsl:value-of select="@repeats"/>
            <xsl:text>",&#xd;</xsl:text>
            <xsl:text>"roundup": "</xsl:text>
            <xsl:value-of select="@roundUp"/>
            <xsl:text>"}</xsl:text>
            <xsl:if test="position() != last()">
                <xsl:text>,&#xD;</xsl:text>
            </xsl:if>
        </xsl:for-each>-->
    </xsl:template>

    <xsl:template match="gc:conditionGroups|cat:conditionGroups">
        <xsl:apply-templates select="gc:conditions|cat:conditions"/>
        <xsl:text>,&#xd;</xsl:text>
        <xsl:apply-templates select="gc:conditionGroups|cat:conditionGroups"/>
    </xsl:template>

    <xsl:template match="gc:modifiers|cat:modifiers">
        <xsl:text>"modifiers": [&#xd;</xsl:text>
        <!--<xsl:for-each select="gc:modifier|cat:modifier">
            <xsl:text>{</xsl:text>
            <xsl:if test="gc:conditions|gc:conditionGroups|cat:conditions|cat:conditionGroups">
                <xsl:apply-templates select="gc:conditions|cat:conditions"/>
                <xsl:apply-templates select="gc:conditionGroups|cat:conditionGroups"/>
            </xsl:if>
            <xsl:text>"type": "</xsl:text>
            <xsl:value-of select="@type"/>
            <xsl:text>",&#xd;</xsl:text>
            <xsl:text>"field": "</xsl:text>
            <xsl:value-of select="@field"/>
            <xsl:text>",&#xd;</xsl:text>
            <xsl:text>"value": "</xsl:text>
            <xsl:choose>
                <xsl:when test="string(number(myNode)) != 'NaN'">
                    <xsl:value-of select="round(@value)"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="@value"/>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:text>",&#xd;</xsl:text>
            <xsl:text>"repeats": [&#xd;</xsl:text>
            <xsl:apply-templates select="gc:repeats|cat:repeats"/>
            <xsl:text>]&#xd;</xsl:text>
            <xsl:text>}</xsl:text>
            <xsl:if test="position() != last()">
                <xsl:text>,&#xD;</xsl:text>
            </xsl:if>
        </xsl:for-each>-->
        <xsl:text>]&#xd;</xsl:text>
    </xsl:template>

    <xsl:template match="gc:modifierGroups|cat:modifierGroups">
        <xsl:text>"modifiers_groups": [&#xd;</xsl:text>
        <xsl:for-each select="gc:modifierGroup|cat:modifierGroup">
            <xsl:text>{</xsl:text>
            <xsl:text>}</xsl:text>
            <xsl:if test="position() != last()">
                <xsl:text>,&#xD;</xsl:text>
            </xsl:if>
        </xsl:for-each>
        <xsl:text>]&#xd;</xsl:text>
    </xsl:template>
</xsl:stylesheet>
