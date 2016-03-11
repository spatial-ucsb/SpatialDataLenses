package geog288;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

import javax.imageio.ImageIO;

public class EventConstructor {
	 
	static short[][] difference9601 = new short[41827][20860];
	static short[][] difference0106 = new short[41827][20860];
	static short[][] difference0610 = new short[41827][20860];
	static ArrayList<CCEvent> events = new ArrayList<CCEvent>();
	
	public static void main(String[] args) throws IOException{
		String root = "C:\\Users\\Behzad\\Documents\\Course Matrerial\\GEOG 288\\Land Cover Change\\PNG Images\\";
		
		Runtime runtime = Runtime.getRuntime();
		//System.out.println((runtime.totalMemory()/(1024*1024)));
		
		BufferedImage image1996 = ImageIO.read(new File(root+"ca_1996_land_cover1.png"));
		BufferedImage image2001 = ImageIO.read(new File(root+"ca_2001_land_cover1.png"));
		BufferedImage image2006 = ImageIO.read(new File(root+"ca_2006_land_cover1.png"));
		BufferedImage image2010 = ImageIO.read(new File(root+"ca_2010_land_cover1.png"));
		
		
		//System.out.println((runtime.totalMemory()/(1024*1024)));
				
		FileWriter writer9601 = new FileWriter(root+"difference9601.csv");
		FileWriter writer0106 = new FileWriter(root+"difference0106.csv");
		FileWriter writer0610 = new FileWriter(root+"difference0610.csv");
	
		int templocation[] = new int[2];
		
		for (int i=0;i<image1996.getHeight();i++){
			for(int j=0; j<image1996.getWidth(); j++){
				difference9601[i][j] = (short)(image2001.getRGB(j, i) - image1996.getRGB(j,i));
				if (difference9601[i][j]!=0){
					templocation[0] = i;
					templocation[1] = j;
					events.add(new CCEvent(templocation, image1996.getRGB(j,i), image2001.getRGB(j, i), 1996, 2001));
				}				
				writer9601.append(String.valueOf(difference9601[i][j]) + ',');

				difference0106[i][j] = (short)(image2006.getRGB(i, j) - image2001.getRGB(i,j));
				if (difference0106[i][j]!=0){
					templocation[0] = i;
					templocation[1] = j;
					events.add(new CCEvent(templocation, image2001.getRGB(j,i), image2006.getRGB(j, i), 2001, 2006));
				}				
				writer0106.append(String.valueOf(difference0106[i][j]) + ',');
				
				difference0610[i][j] = (short)(image2010.getRGB(i, j) - image2006.getRGB(i,j));
				if (difference0610[i][j]!=0){
					templocation[0] = i;
					templocation[1] = j;
					events.add(new CCEvent(templocation, image2006.getRGB(j,i), image2010.getRGB(j, i), 2006, 2010));
				}				
				writer0610.append(String.valueOf(difference0610[i][j]) + ',');
			}
			writer9601.append("\n");
			writer0106.append("\n");
			writer0610.append("\n");
		}
		
		writer9601.flush();
		writer9601.close();
		
		writer0106.flush();
		writer0106.close();
		
		writer0610.flush();
		writer0610.close();
		
		System.out.println("done!");
		System.out.println(events.size());
	}
	
	
}
