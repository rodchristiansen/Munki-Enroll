<?php
namespace CFPropertyList;

require_once( 'template/CFPropertyList.php' );

// Get the varibles passed by the enroll script
$catalog = $_GET["catalog"];
$area = $_GET["area"];
$room = $_GET["room"];
$asset = $_GET["asset"];
$hostname = $_GET["hostname"];

// Create manifest for catalog
//
if ( file_exists( '../manifests/' . $catalog . '/' . $catalog . 'Machines' ) )
    {
        echo "\n";
        echo "Manifest for catalog $catalog already exists. \n\n";
    }
else
    {
        echo "\n";
        echo "Manifest for catalog $catalog does not exist. Creating ... \n\n";
        
        if ( !is_dir( '../manifests/' . $catalog . '/' ) )
            {
                mkdir( '../manifests/' . $catalog . '/', 0755, true );
            }

        // Create the new manifest plist
        $plist = new CFPropertyList();
        $plist->add( $dict = new CFDictionary() );
        
        // Save the newly created plist
        $plist->saveXML( '../manifests/' . $catalog . '/' . $catalog . 'Machines' );
        
    }

// Create manifest for area
//
if ( file_exists( '../manifests/' . $catalog . '/' . $area . '/' . $area ) )
    {
        echo "Manifest for area $area already exists. \n\n";
    }
else
    {
        echo "Manifest for area $area does not exist. Creating ... \n\n";
        
        if ( !is_dir( '../manifests/' . $catalog . '/' . $area . '/' ) )
            {
                mkdir( '../manifests/' . $catalog . '/' . $area . '/', 0755, true );
            }

        // Create the new manifest plist
        $plist = new CFPropertyList();
        $plist->add( $dict = new CFDictionary() );

        // Add parent manifest to included_manifests to achieve waterfall effect
        $dict->add( 'included_manifests', $array = new CFArray() );
        $array->add( new CFString( $catalog . '/' . $catalog . 'Machines' ) );
        
        // Save the newly created plist
        $plist->saveXML( '../manifests/' . $catalog . '/' . $area . '/' . $area );
        
    }

// Create manifest for Room
//
if ( file_exists( '../manifests/' . $catalog . '/' . $area . '/' . $area . $room ) )
    {
		echo "";
        echo "Manifest for room $room already exists. \n\n";
		echo "";
    }
else
    {
		echo "";
        echo "Manifest for room $room does not exist. Creating ... \n\n";
		echo "";
        
        if ( !is_dir( '../manifests/' . $catalog . '/' . $area . '/' ) )
            {
                mkdir( '../manifests/' . $catalog . '/' . $area . '/' , 0755, true );
            }

        // Create the new manifest plist
        $plist = new CFPropertyList();
        $plist->add( $dict = new CFDictionary() );
        
        // Add parent manifest to included_manifests to achieve waterfall effect
        $dict->add( 'included_manifests', $array = new CFArray() );
        $array->add( new CFString( $catalog . '/' . $catalog . 'Machines' ) );
        $array->add( new CFString( $catalog . '/' . $area . '/' . $area ) );
        
        // Save the newly created plist
        $plist->saveXML( '../manifests/' . $catalog . '/' . $area . '/' . $area . $room );
        
    }


// Create manifest for a single machine and set it
//
if ( file_exists( '../manifests/' . $catalog . '/' . $area . '/' . $hostname ) )
    {
        echo "Manifest for machine $hostname already exists. \n\n";
    }
else
    {
        echo "Manifest for machine $hostname does not exist. Creating ... \n\n";

        // Create the new manifest plist
        $plist = new CFPropertyList();
        $plist->add( $dict = new CFDictionary() );

        // Add catalog catalog
        $dict->add( 'catalogs', $array = new CFArray() );
        $array->add( new CFString( $catalog ) );
        
        // Add parent manifest to included_manifests to achieve waterfall effect
        $dict->add( 'included_manifests', $array = new CFArray() );
        $array->add( new CFString( $catalog . '/' . $catalog . 'Machines' ) );
        $array->add( new CFString( $catalog . '/' . $area . '/' . $area ) );
        $array->add( new CFString( $catalog . '/' . $area . '/' . $area . $room ) );
        
        // Save the newly created plist
        $plist->saveXML( '../manifests/' . $catalog . '/' . $area . '/' . $hostname );
        
    }


?>
