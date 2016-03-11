package geog288;

import java.util.Calendar;

public class CCEvent {
	private int timeInterval;
	private int[] location = new int[2];
	private String initialClass, finalClass;
	//private CoreConcepts inputConcept;
	private String conceptType;
	
	public CCEvent(int[] location, int initialClass, int finalClass, int startTime, int endTime){
//		if (inputConcept instanceof CCField) conceptType = ((CCField)inputConcept).GetConceptType();
//		else if (inputConcept instanceof CCObject) conceptType = ((CCObject)inputConcept).GetConceptType();
		
		this.location = location;
		String classDifference = infereClass(initialClass,finalClass);
		this.timeInterval = startTime - endTime;
		
	}

	private String infereClass(int initialClass2, int finalClass2) {
		// TODO Auto-generated method stub
		return null;
	}
	
	/*public boolean isInside (int[][]location, CCObject county){
		return false;
	}*/
	
}
